from dataclasses import dataclass, field
from typing import List
import random
from poker_engine import create_deck



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