from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from poker_engine import create_deck, best_of_7, compare
from ai_player import ai_decide
import random
from game_state import Gamestate


game = Gamestate() # Global Spilltilsand
game.reset_table(num_ai=1) # Lager 1 AI-spiller eller flere


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/deal")
def deal_hand():
 
    game.shuffle_and_deal()

    return {
        "message": "hand_dealt",
        "players": [
            {
                "id": p.id,
                "name": p.name,
                "chips": p.chips,
                "hand": p.hand if not p.ai else ["??", "??"], # Skjuler AI kort
                "folded": p.folded,
                "current_bet": p.current_bet,
                "total_bet": p.total_bet
            }
            for p in game.players
        ],
        "board": game.board,
        "street": game.street,
        "pot": game.pot,
        "dealer_idx": game.dealer_idx,
        "current_idx": game.current_idx
    }


# Endpoint for resett/start av spill
@app.post("/start")
def start_game(num_ai: int = 1, starting_chips: int = 1000):
    game.reset_table(num_ai=num_ai, starting_chips=starting_chips)
    game.shuffle_and_deal()

    return {
        "message": "new_game_started",
        "players": [vars(p) for p in game.players],
        "board": game.board,
        "street": game.street,
        "pot": game.pot
    }

# Endpoint for spiller handlinger
@app.post("/action")
def take_action(player_id: int, action: str, amount: int = 0):


    result = game.player_action(player_id, action, amount)


    if not game.players[1].folded and game.current_idx == 1:
        ai_move = ai_decide(
            hole=game.players[1].hand,
            board=game.board,
            stage=game.street
        )
        game.player_action(1, ai_move)


    return {
        "action_result": result,
        "players": [vars(p) for p in game.players],
        "board": game.board,
        "street": game.street,
        "pot": game.pot
    }

# Endpoint for å hente ut gamestate
@app.get("/state")
def get_state():
    return {
        "players": [vars(p) for p in game.players],
        "board": game.board,
        "street": game.street,
        "pot": game.pot,
        "current_idx": game.current_idx
    }