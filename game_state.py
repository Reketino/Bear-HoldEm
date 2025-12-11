from dataclasses import dataclass, field
from typing import List
import random
from poker_engine import create_deck, best_of_7



@dataclass #1
class Player:
    id: int
    name: str
    chips: int = 1000
    ai: bool = False
    hand: List[str] = field(default_factory=list)
    folded: bool = False
    current_bet: int = 0
    total_bet: int = 0



@dataclass #2
class Gamestate:
    players: List[Player] = field(default_factory=list)
    deck: List [str] = field(default_factory=list)
    board: List [str] = field(default_factory=list)
    pot: int = 0
    street: str = "preflop" #klasser evnt => | preflop | flop | turn | river | showdown
    dealer_idx: int = 0
    current_idx: int = 0
    big_blind: int = 20
    small_blind: int = 10
    to_call: int = 0
    last_raiser_idx: int = -1

   #Reset bord
    def reset_table(self, num_ai=1, starting_chips=1000):
        self.players = []
        # Player 0 er Menneske
        self.players.append(Player(id=0, name="You", chips=starting_chips, ai=False))
        for i in range(num_ai):
            self.players.append(Player(id=1+i, name=f"AI_{i+1}", chips=starting_chips, ai=True))
        self.deck = []
        self.board = []
        self.pot = 0
        self.street = "preflop"
        self.dealer_idx = 0
        self.current_idx = (self.dealer_idx + 1) % len(self.players)
        self.to_call = 0
        self.last_raiser_idx = -1


    def shuffle_and_deal(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        # Klarerer hender
        for p in self.players:
            p.hand = []
            p.folded = False
            p.current_bet = 0
            p.total_bet = 0
        # Dealer 2 kort hver
        for _ in range(2):
            for p in self.players:
                p.hand.append(self.deck.pop())
        self.board = []
        self.pot = 0
        self.street = "preflop"
        # blinds
        sb_idx = (self.dealer_idx + 1) % len(self.players)
        bb_idx = (self.dealer_idx + 2) % len(self.players)
        sb = self.small_blind
        bb = self.big_blind
        self.players[sb_idx].chips -= sb
        self.players[sb_idx].current_bet = sb
        self.players[sb_idx].total_bet += sb
        self.players[bb_idx].chips -= bb
        self.players[bb_idx].current_bet = bb
        self.players[bb_idx].total_bet += bb
        self.to_call = bb
        # Etter big blind er "player" først ut
        self.current_idx = (bb_idx + 1) % len(self.players)
        self.last_raiser_idx = bb_idx


    def player_action(self, player_id, action, amount=0):
        player = self.players[player_id]

        if player.folded:
            return "Player already folded"
        
        if action == "fold":
            player.folded = True
            return "fold"
        
        if action == "check":
            if player.current_bet == self.to_call:
                return "check"
            else:
                return "cannot_check"
            
        if action == "call":
            to_pay = self.to_call - player.current_bet
            to_pay = min(to_pay, player.chips) #All in
            player.chips -= to_pay
            player.current_bet += to_pay
            player.total_bet += to_pay
            return "call"
        
        if action == "raise":
            if amount <= self.to_call:
                return "invalid_raise"
            
            raise_amount = amount - player.current_bet
            if raise_amount > player.chips:
                return "not_enough_chips"
            

            player.chips -= raise_amount
            player.current_bet = amount
            player.total_bet += raise_amount


            self.to_call = amount
            self.last_raiser_idx = player_id
            return "raise"
        

        if action == "allin":
            amount = player.chips + player.current_bet
            player.total_bet += player.chips
            player.chips = 0
            player.current_bet = amount


            if amount > self.to_call:
                self.to_call = amount
                self.last_raiser_idx = player_id


            return "allin"
        
        return "unknown_action"
    

    def advance_street(self):
        for p in self.players:
            self.pot += p.current_bet
            p.current_bet = 0

        self.to_call = 0
        self.last_raiser_idx = -1


        if self.street == "preflop":
            # 3 kort flop
            self.board = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
            self.street = "flop"

    
        elif self.street == "flop":
            self.board.append(self.deck.pop())
            self.street = "turn"


        elif self.street == "turn":
            self.board.append(self.deck.pop())
            self.street = "river"


        elif self.street == "river":
            self.street = "showdown"
            return "showdown"
        
        # current_idx blir satt til første spiller etter dealer
        self.current_idx = (self.dealer_idx + 1) % len(self.players)

        # Finner første spiller som ikke foldet
        while self.players[self.current_idx].folded:
            self.current_idx = (self.current_idx + 1) % len(self.players)

        return self.street
    

    def is_betting_round_finished(self):
        active_players = [p for p in self.players if not p.folded]

        # Hånd ferdig vist det bare er en spiller igjen
        if len(active_players) <= 1:
            return True
        
        # Hente aktuelle bets
        active_bets = [p.current_bet for p in active_players]

        if len(set(active_bets)) == 1:
            if self.last_raiser_idx == -1:
                return True
            
        if self.current_idx == self.last_raiser_idx:
            return True
        
        return False
    

    def showdown(self):
        #funksjon for å samle spillere som ikke har foldet
        active_players = [p for p in self.players if not p.folded]

        #En spiller igjen?-automatisk vinner
        if len (active_players) == 1:
            winner = active_players[0]
            return {
                "winner_id": winner.id,
                "winner_name": winner.name,
                "winner_hand": None,
                "players": [
                    {"id": p.id, "name": p.name, "hand": p.hand, "folded": p.folded}
                    for p in self.players
                ],
            }
        

        # Hver spiller blir evaluert her med "bof7"
        results = []
        for p in active_players:
            score, hand_name = best_of_7(p.hand, self.board)
            results.append({
                "id": p.id,
                "name": p.name,
                "hand": p.hand, 
                "score": score,
                "hand_name": hand_name
            })

        # Sortering av score, høyste score først
        results.sort(key=lambda x: x["score"], reverse=True)
        winner = results[0]


        return {
            "winner_id":winner["id"],
            "winner_name": winner["name"],
            "winner_hand": winner["hand_name"],
            "players": results
        }    
