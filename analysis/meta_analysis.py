def analyze_meta(rankings):
    for r in rankings:
        score = (
            r["win_rate"] * 0.5 +
            r["pick_rate"] * 0.3 -
            r["ban_rate"] * 0.2
        )
        r["meta_score"] = round(score, 2)

        if r["win_rate"] > 55 and r["ban_rate"] > 20:
            r["meta"] = "Overpowered"
        elif r["win_rate"] > 52:
            r["meta"] = "Strong"
        elif r["win_rate"] < 48:
            r["meta"] = "Weak"
        else:
            r["meta"] = "Balanced"

    return rankings
