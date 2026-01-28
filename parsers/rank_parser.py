import json


def parse_rank_table(raw):
    result = []
    
    # Parse API response from gms.moontontech.com
    data = None
    if hasattr(raw, 'json'):
        try:
            data = raw.json()
        except:
            pass
    elif isinstance(raw, dict):
        data = raw
    
    # API returns {data: {data: {records: [...]}}}
    if data and isinstance(data, dict) and 'data' in data:
        data_obj = data.get('data', {})
        if isinstance(data_obj, dict) and 'data' in data_obj:
            # Nested data structure
            data_obj = data_obj.get('data', {})
        
        if isinstance(data_obj, dict) and 'records' in data_obj:
            records = data_obj['records']
            
            for record in records:
                record_data = record.get('data', {})
                if not isinstance(record_data, dict):
                    continue
                
                # Get counter heroes
                counters = []
                sub_heroes = record_data.get('sub_hero', [])
                if isinstance(sub_heroes, list):
                    for sub_hero in sub_heroes[:3]:  # Top 3 counters
                        hero_channel = sub_hero.get('hero_channel', {})
                        if isinstance(hero_channel, dict):
                            counters.append({
                                'heroid': str(sub_hero.get('heroid', '')),
                                'channelid': str(hero_channel.get('id', '')),
                                'increase_win_rate': sub_hero.get('increase_win_rate', 0)
                            })
                
                main_hero = record_data.get('main_hero', {})
                hero_data = {}
                if isinstance(main_hero, dict):
                    hero_data = main_hero.get('data', {})
                    if not isinstance(hero_data, dict):
                        hero_data = {}
                
                result.append({
                    "heroid": str(record_data.get('main_heroid', '')),
                    "name": hero_data.get('name', ''),
                    "pick_rate": record_data.get('main_hero_appearance_rate', 0),
                    "win_rate": record_data.get('main_hero_win_rate', 0),
                    "ban_rate": record_data.get('main_hero_ban_rate', 0),
                    "tier": None,
                    "counters": json.dumps(counters) if counters else None
                })
            
            return result
    
    # Fallback: old format or HTML
    if data and isinstance(data, dict) and "data" in data:
        data_inner = data.get("data", {})
        if isinstance(data_inner, dict) and "list" in data_inner:
            for r in data_inner["list"]:
                result.append({
                    "heroid": r["hero_id"],
                    "name": r["hero_name"],
                    "pick_rate": r["pick_rate"],
                    "win_rate": r["win_rate"],
                    "ban_rate": r["ban_rate"],
                    "tier": r.get("tier"),
                    "counters": None
                })
    
    return result
