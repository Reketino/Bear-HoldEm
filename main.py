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
    deck = create_deck()
    random.shuffle(deck)


    player = [deck.pop(), deck.pop()]
    ai = [deck.pop(), deck.pop()]
    board = [deck.pop() for _ in range(5)]
    ai_action = ai_decide(ai, board[:0], "preflop", bluff_enabled=True)


    result = compare(player, ai, board)

    return {
        "player": player,
        "ai": ["??", "??"],
        "board": board,
        "winner": result,
        "ai_action": ai_action
    }