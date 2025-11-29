from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from poker_engine import create_deck, best_of_7, compare
import random


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
    opponent = [deck.pop(), deck.pop()]
    board = [deck.pop() for _ in range(5)]


    result = compare(player, opponent, board)

    return {
        "player": player,
        "opponent": ["??", "??"],
        "board": board,
        "winner": result
    }