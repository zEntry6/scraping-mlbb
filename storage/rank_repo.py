from storage.db import get_connection
from datetime import datetime

def save_rank_snapshot(rankings):
    conn = get_connection()
    cur = conn.cursor()

    snapshot_date = datetime.utcnow().strftime("%Y-%m-%d")

    for i, r in enumerate(rankings):
        cur.execute("""
        INSERT OR REPLACE INTO hero_rankings
        (snapshot_date, rank, heroid, win_rate, pick_rate, ban_rate, meta_label, counters)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            snapshot_date,
            i + 1,  # Rank based on order
            r["heroid"],
            r["win_rate"],
            r["pick_rate"],
            r["ban_rate"],
            r.get("meta_label"),
            r.get("counters")
        ))

    conn.commit()
    conn.close()
