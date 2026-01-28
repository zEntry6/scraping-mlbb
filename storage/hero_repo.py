from storage.db import get_connection
import json

def upsert_heroes(heroes):
    conn = get_connection()
    cur = conn.cursor()

    for h in heroes:
        cur.execute("""
        INSERT OR REPLACE INTO heroes (heroid, name, role, channelid)
        VALUES (?, ?, ?, ?)
        """, (h["heroid"], h["name"], h["role"], h["channelid"]))

    conn.commit()
    conn.close()


def save_hero_detail(heroid, detail):
    """
    Save hero detail including skills, combos, rates, and counter info
    detail should contain: skills, combos, rates, counter_info
    """
    conn = get_connection()
    cur = conn.cursor()

    # Save rates and counter info to hero_details
    rates = detail.get("rates", {})
    counter_info = detail.get("counter_info", {})
    
    cur.execute("""
    INSERT OR REPLACE INTO hero_details
    (heroid, win_rate, pick_rate, ban_rate, counters, countered_by, synergy)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        heroid,
        rates.get("win_rate", 0.0),
        rates.get("pick_rate", 0.0),
        rates.get("ban_rate", 0.0),
        counter_info.get("counters", ""),
        counter_info.get("countered_by", ""),
        counter_info.get("synergy", "")
    ))

    # Save skills to hero_skills table
    skills = detail.get("skills", [])
    for s in skills:
        cur.execute("""
        INSERT OR REPLACE INTO hero_skills
        (heroid, skill_name, skill_desc, skill_type, cooldown)
        VALUES (?, ?, ?, ?, ?)
        """, (heroid, s["name"], s["desc"], s.get("type", "Active"), s.get("cooldown")))

    # Save combos
    combos = detail.get("combos", [])
    for combo in combos:
        combo_str = json.dumps(combo) if isinstance(combo, (list, dict)) else str(combo)
        cur.execute("""
        INSERT OR REPLACE INTO hero_combos
        (heroid, combo)
        VALUES (?, ?)
        """, (heroid, combo_str))

    conn.commit()
    conn.close()
