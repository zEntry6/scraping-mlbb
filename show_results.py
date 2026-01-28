import sqlite3

conn = sqlite3.connect('mlbb.db')
cur = conn.cursor()

print("="*70)
print("HASIL SCRAPING - SAMPLE 3 HEROES")
print("="*70)

# Ambil Sora, Zetian, Lukas
heroes = cur.execute('''
    SELECT h.heroid, h.name, h.role, 
           d.win_rate, d.pick_rate, d.ban_rate,
           d.counters, d.countered_by, d.synergy
    FROM heroes h
    LEFT JOIN hero_details d ON h.heroid = d.heroid
    WHERE h.name IN ('Sora', 'Zetian', 'Lukas')
    ORDER BY h.heroid DESC
''').fetchall()

for hero in heroes:
    heroid, name, role, win, pick, ban, counters, countered_by, synergy = hero
    
    print(f"\n{'='*70}")
    print(f"{name} (ID: {heroid}) - {role}")
    print('='*70)
    
    if win is not None:
        print(f"\n📊 RATES:")
        print(f"  Win:  {win*100:.2f}%")
        print(f"  Pick: {pick*100:.2f}%")
        print(f"  Ban:  {ban*100:.2f}%")
    
    if counters:
        print(f"\n⚔️  MENG-COUNTER:")
        print(f"  {counters}")
    
    if countered_by:
        print(f"\n🛡️  DI-COUNTER OLEH:")
        print(f"  {countered_by}")
    
    if synergy:
        print(f"\n🤝 KECOCOKAN:")
        print(f"  {synergy}")
    
    # Show skills
    skills = cur.execute('''
        SELECT skill_name, skill_type 
        FROM hero_skills 
        WHERE heroid = ?
    ''', (heroid,)).fetchall()
    
    if skills:
        print(f"\n🎯 SKILLS ({len(skills)}):")
        for skill_name, skill_type in skills:
            print(f"  • {skill_name} ({skill_type})")

# Get total counts
total_heroes = cur.execute('SELECT COUNT(*) FROM heroes').fetchone()[0]
total_details = cur.execute('SELECT COUNT(*) FROM hero_details').fetchone()[0]
total_skills = cur.execute('SELECT COUNT(*) FROM hero_skills').fetchone()[0]

print("\n" + "="*70)
print(f"✅ TOTAL: {total_heroes} heroes, {total_details} details, {total_skills} skills tersimpan di mlbb.db")
print("="*70)

conn.close()
