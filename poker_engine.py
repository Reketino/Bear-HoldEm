
from itertools import combinations

RANKS = '23456789TJQKA'
SUITS = 'SHDC'

RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}


Hand_RANKS = {
    9: "Royal Flush",
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card",
}



def create_deck():
    return [r+s for r in RANKS for s in SUITS]



def evaluate_5(cards):
    values = sorted([RANK_VALUES[c[0]]  for c in cards], reverse= True)
    suits = [c[1] for c in cards]
    
    
    is_flush = len(set(suits)) == 1
    
    
    unique = sorted(set(values), reverse=True)
    is_straight = False
    
    
    if len(unique) >= 5:
        for i in range(len(unique) - 4):
            if unique[i] - unique[i + 4] == 4:
                is_straight = True
                straight_high = unique[i]
                break
        
        else:
            if set([14, 5, 4, 3, 2]).issubset(set(unique)):
                is_straight = True
                straight_high = 5
                
    else:
        straight_high = None
        
    
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
        
        
    pattern = sorted(counts.values(), reverse=True)
    
    
    
    if is_straight and is_flush and straight_high == 14:
        rank = 9
    elif is_straight and is_flush:
        rank = 8
    elif 4 in pattern:
        rank = 7
    elif pattern == [3, 2]:
        rank = 6
    elif is_flush:
        rank = 5
    elif is_straight:
        rank = 4
    elif 3 in pattern:
        rank = 3
    elif pattern == [2, 2, 1]:
        rank = 2
    elif 2 in pattern:
        rank = 1
    else:
        rank = 0
        
    return rank, values



def best_of_7(hole, board):
    best = None
    
    
    for combo in combinations(hole + board, 5):
        rank, values = evaluate_5(combo)
        
        
        if best is None or (rank, values) > (best["rank"], best["values"]):
            best = {
                "rank": rank,
                "values": values,
                "hand_name": Hand_RANKS[rank],
            }
            
    return best["rank"], best["hand_name"]



def compare(player_hand, opponent_hand, board):
    p_rank, _ = best_of_7(player_hand, board)
    o_rank, _ = best_of_7(opponent_hand, board)
    
    if p_rank > o_rank:
        return "player"
    if o_rank > p_rank:
        return "opponent"
    return "tie"