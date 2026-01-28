import sqlite3
from config.settings import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Hero master
    cur.execute("""
    CREATE TABLE IF NOT EXISTS heroes (
        heroid INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        channelid INTEGER
    )
    """)

    # Hero detail
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hero_details (
        heroid INTEGER PRIMARY KEY,
        win_rate REAL,
        pick_rate REAL,
        ban_rate REAL,
        counters TEXT,
        countered_by TEXT,
        synergy TEXT
    )
    """)
    
    # Hero skills
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hero_skills (
        heroid INTEGER,
        skill_name TEXT,
        skill_desc TEXT,
        skill_type TEXT,
        cooldown TEXT,
        PRIMARY KEY (heroid, skill_name)
    )
    """)

    # Hero combo
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hero_combos (
        heroid INTEGER,
        combo TEXT,
        PRIMARY KEY (heroid, combo)
    )
    """)

    # Ranking snapshot
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hero_rankings (
        snapshot_date TEXT,
        rank INTEGER,
        heroid INTEGER,
        win_rate REAL,
        pick_rate REAL,
        ban_rate REAL,
        meta_label TEXT,
        counters TEXT,
        PRIMARY KEY (snapshot_date, heroid)
    )
    """)

    conn.commit()
    conn.close()
