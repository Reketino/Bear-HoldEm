import random
from itertools import combinations

RANKS = '23456789TJQKA'
SUITS = 'SHDC'

def create_deck():
    return [r+s for r in RANKS for s in SUITS]


def evaluate_5(cards):

    ranks_map = {r:i for i,r in enumerate(RANKS,start=2)}
    vals = sorted([ranks_map[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    is_flush = len(set(suits)) == 1

    # Oppsett for "Straight"
    uniq = sorted(set(vals), reverse=True)
    straight = False
    if len(uniq)>= 5:
        for i in range(len(uniq)-4):
            if uniq[i] - uniq[i+4] == 4:
                straight = True



    counts = {}
    for v in vals:
        counts[v] = counts.get(v,0) + 1
    pattern = sorted(counts.values(), reverse=True)


    #Rangering av styrke på hender (0-8)
    if straight and is_flush: rank = 8
    elif 4 in pattern: rank = 7
    elif pattern == [3,2]: rank = 6
    elif is_flush: rank = 5
    elif straight: rank = 4
    elif 3 in pattern: rank = 3
    elif pattern == [2,2,1]: rank = 2
    elif 2 in pattern: rank = 1
    else: rank = 0


    return (rank, vals)      


def best_of_7(hole, board):
    best = None
    for combo in combinations(hole+board, 5):
        r = evaluate_5(combo)
        if best is None or r > best:
            best = r
    return best


def compare (player, opponent, board):
    p = best_of_7(player, board)
    o = best_of_7(opponent, board)
    if p > o: return "player"
    if o > p: return "opponent"
    return "tie"