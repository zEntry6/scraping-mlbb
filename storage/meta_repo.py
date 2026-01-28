from storage.db import get_connection
from datetime import datetime

def save_meta_results(meta_results):
    conn = get_connection()
    cur = conn.cursor()

    snapshot_date = datetime.utcnow().strftime("%Y-%m-%d")

    for h in meta_results:
        cur.execute("""
        UPDATE hero_rankings
        SET meta_label = ?
        WHERE heroid = ? AND snapshot_date = ?
        """, (h["meta_label"], h["heroid"], snapshot_date))

    conn.commit()
    conn.close()
