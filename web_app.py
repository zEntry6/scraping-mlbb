from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('mlbb.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/heroes')
def get_heroes():
    conn = get_db()
    cur = conn.cursor()
    
    heroes = cur.execute('''
        SELECT h.heroid, h.name, h.role, h.channelid,
               d.win_rate, d.pick_rate, d.ban_rate,
               d.counters, d.countered_by, d.synergy
        FROM heroes h
        LEFT JOIN hero_details d ON h.heroid = d.heroid
        ORDER BY h.heroid DESC
    ''').fetchall()
    
    result = []
    for hero in heroes:
        # Get skills
        skills = cur.execute('''
            SELECT skill_name, skill_desc, skill_type, cooldown
            FROM hero_skills
            WHERE heroid = ?
        ''', (hero['heroid'],)).fetchall()
        
        # Get combo
        combo = cur.execute('''
            SELECT combo
            FROM hero_combos
            WHERE heroid = ?
        ''', (hero['heroid'],)).fetchone()
        
        result.append({
            'heroid': hero['heroid'],
            'name': hero['name'],
            'role': hero['role'],
            'channelid': hero['channelid'],
            'win_rate': round(hero['win_rate'] * 100, 2) if hero['win_rate'] else None,
            'pick_rate': round(hero['pick_rate'] * 100, 2) if hero['pick_rate'] else None,
            'ban_rate': round(hero['ban_rate'] * 100, 2) if hero['ban_rate'] else None,
            'counters': hero['counters'],
            'countered_by': hero['countered_by'],
            'synergy': hero['synergy'],
            'skills': [dict(s) for s in skills],
            'combo': combo['combo'] if combo else None
        })
    
    conn.close()
    return jsonify(result)

@app.route('/api/hero/<int:heroid>')
def get_hero(heroid):
    conn = get_db()
    cur = conn.cursor()
    
    hero = cur.execute('''
        SELECT h.heroid, h.name, h.role, h.channelid,
               d.win_rate, d.pick_rate, d.ban_rate,
               d.counters, d.countered_by, d.synergy
        FROM heroes h
        LEFT JOIN hero_details d ON h.heroid = d.heroid
        WHERE h.heroid = ?
    ''', (heroid,)).fetchone()
    
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    skills = cur.execute('''
        SELECT skill_name, skill_desc, skill_type, cooldown
        FROM hero_skills
        WHERE heroid = ?
    ''', (heroid,)).fetchall()
    
    combo = cur.execute('''
        SELECT combo
        FROM hero_combos
        WHERE heroid = ?
    ''', (heroid,)).fetchone()
    
    result = {
        'heroid': hero['heroid'],
        'name': hero['name'],
        'role': hero['role'],
        'channelid': hero['channelid'],
        'win_rate': round(hero['win_rate'] * 100, 2) if hero['win_rate'] else None,
        'pick_rate': round(hero['pick_rate'] * 100, 2) if hero['pick_rate'] else None,
        'ban_rate': round(hero['ban_rate'] * 100, 2) if hero['ban_rate'] else None,
        'counters': hero['counters'],
        'countered_by': hero['countered_by'],
        'synergy': hero['synergy'],
        'skills': [dict(s) for s in skills],
        'combo': combo['combo'] if combo else None
    }
    
    conn.close()
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    
    total_heroes = cur.execute('SELECT COUNT(*) FROM heroes').fetchone()[0]
    total_details = cur.execute('SELECT COUNT(*) FROM hero_details').fetchone()[0]
    total_skills = cur.execute('SELECT COUNT(*) FROM hero_skills').fetchone()[0]
    total_combos = cur.execute('SELECT COUNT(*) FROM hero_combos').fetchone()[0]
    heroes_with_counter = cur.execute('SELECT COUNT(*) FROM hero_details WHERE counters IS NOT NULL').fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_heroes': total_heroes,
        'total_details': total_details,
        'total_skills': total_skills,
        'total_combos': total_combos,
        'heroes_with_counter': heroes_with_counter
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
