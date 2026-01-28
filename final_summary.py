import sqlite3

conn = sqlite3.connect('mlbb.db')
cur = conn.cursor()

print('='*70)
print('DATA YANG SUDAH DI-SCRAPE')
print('='*70)

# 1. Heroes
hero_count = cur.execute('SELECT COUNT(*) FROM heroes').fetchone()[0]
print(f'\n✅ 1. HEROES: {hero_count} heroes')
print('   - heroid, name, role, channelid')

# 2. Hero details (rates)
detail_count = cur.execute('SELECT COUNT(*) FROM hero_details').fetchone()[0]
print(f'\n✅ 2. RATES: {detail_count} heroes')
print('   - Win Rate, Pick Rate, Ban Rate')

# 3. Counter data
counter_count = cur.execute('SELECT COUNT(*) FROM hero_details WHERE counters IS NOT NULL AND counters != ""').fetchone()[0]
print(f'\n⚠️  3. COUNTER DATA: {counter_count} heroes')
heroes_with_counter = cur.execute('SELECT heroid FROM hero_details WHERE counters IS NOT NULL AND counters != "" ORDER BY heroid DESC').fetchall()
counter_ids = [h[0] for h in heroes_with_counter]
print(f'   - Hero IDs: {counter_ids}')
print('   - Meng-Counter, Di-Counter oleh, Kecocokan')

# 4. Skills
skill_count = cur.execute('SELECT COUNT(*) FROM hero_skills').fetchone()[0]
unique_heroes_with_skills = cur.execute('SELECT COUNT(DISTINCT heroid) FROM hero_skills').fetchone()[0]
print(f'\n✅ 4. SKILLS: {skill_count} skills dari {unique_heroes_with_skills} heroes')
print('   - Filtered by hero name (tidak tercampur)')

# 5. Combos
combo_count = cur.execute('SELECT COUNT(*) FROM hero_combos').fetchone()[0]
print(f'\n✅ 5. COMBOS: {combo_count} skill combinations')

print('\n' + '='*70)
print('RINGKASAN FINAL')
print('='*70)
print(f'✅ {hero_count} heroes LENGKAP (heroid, name, role, channelid)')
print(f'✅ {detail_count} heroes dengan Win/Pick/Ban rates')
print(f'✅ {skill_count} skills (filtered per hero)')
print(f'✅ {combo_count} skill combos')
print(f'⚠️  {counter_count} heroes dengan counter data (ID: {counter_ids})')
print(f'\n❌ Counter untuk {hero_count - counter_count} heroes lama TIDAK TERSEDIA')
print('   Alasan: Mobile Legends official API hanya provide untuk 6 heroes terbaru')

print('\n' + '='*70)
print('FILE DATABASE: mlbb.db')
print('='*70)
print('Tables: heroes, hero_details, hero_skills, hero_combos')

conn.close()
