from poker_engine import best_of_7


def ai_decide(hole, board, stage):


    strong_pairs = ["AA", "KK", "QQ", "JJ"]
    connected = ["AK", "AQ", "AJ", "KQ", "KJ", "QJ"]


    ranks = "23456789TJQKA"
    h1, h2 = hole[0][0], hole[1][0]
    pair = h1 == h2


    if stage == "preflop":
        combo = h1 + h2 if h1 >= h2 else h2 + h1


        if pair and combo in strong_pairs:
            return "raise"
        if combo in connected:
            return "call"
        return "fold"
    

    score = best_of_7(hole, board)[0]


    if score >= 6:
        return "allin"
    if score >= 3:
        return "raise"
    if score >= 1:
        return "call"
    return "fold"