import random
from poker_engine import best_of_7

# DECISION LOGIC BEHIND AI'S ACTIONS
def ai_decide(hole, board, stage, bluff_enabled=True):

    # AI'S BLUFFING LOGIC
    if bluff_enabled and stage != "preflop":
        if random.random() < 0.15:
            return "raise"
        if random.random() < 0.05:
            return "allin"
        
    # RANGES OF HANDS
    strong_pairs = ["AA", "KK", "QQ", "JJ"]
    connected = ["AK", "AQ", "AJ", "KQ", "KJ", "QJ"]
    playable = connected + ["AT", "KT", "QT", "JT", "T9", "98", "87"]


    # PARSING OF HOLE CARD
    h1, h2 = hole[0][0], hole[1][0]
    pair = h1 == h2

    # LOGIC IN PREFLOP
    if stage == "preflop":
        combo = h1 + h2 if h1 >= h2 else h2 + h1

        # PREMIUM PAIRS
        if pair and combo in strong_pairs:
            return "raise"
        
        # ALL OTHER PAIRS
        if pair: 
            return "call"
        
        # BROADWAYS STRONG
        if combo in connected:
            return "call"
        
        # PLAYABLE HANDS
        if combo in playable:
            return "call"
        
        # LOOSE CALL FALLBACK
        if random.random() < 0.20:
            return "call"
        
        return "fold"
    
    # LOGIC BEHIND POSTFLOP
    score = best_of_7(hole, board)[0]


    if score >= 6:
        return "allin"
    
    if score >= 3:
        return "raise"
    
    if score >= 1:
        return "call"
    
    # BLUFF WHEN HAVING ALMOST NOTHING
    if random.random() < 0.25:
        return "call"
    
    return "fold"