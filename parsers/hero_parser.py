from lxml import html as lxml_html
import json
import re


def parse_hero_list(raw):
    heroes = []
    
    # If raw is httpx Response with JSON
    if hasattr(raw, 'json'):
        try:
            data = raw.json()
        except:
            data = None
    elif isinstance(raw, dict):
        data = raw
    else:
        data = None
    
    # Parse API response from gms.moontontech.com
    if data and 'data' in data and 'records' in data.get('data', {}):
        records = data['data']['records']
        
        for record in records:
            hero_data = record.get('data', {})
            hero_info = hero_data.get('hero', {}).get('data', {})
            
            # Extract roles from sortid
            roles = []
            for sort_item in hero_info.get('sortid', []):
                if isinstance(sort_item, dict) and 'data' in sort_item:
                    role_title = sort_item['data'].get('sort_title', '')
                    if role_title:
                        roles.append(role_title)
            
            heroes.append({
                "heroid": str(hero_data.get('hero_id', '')),
                "channelid": str(record.get('id', '')),
                "name": hero_info.get('name', ''),
                "role": ', '.join(roles) if roles else 'Unknown'
            })
        
        return heroes
    
    # Fallback: old JSON format
    if data and "data" in data and "list" in data["data"]:
        for h in data["data"]["list"]:
            heroes.append({
                "heroid": h["heroid"],
                "channelid": h["channelid"],
                "name": h["name"],
                "role": h.get("role")
            })
        return heroes
    
    # Fallback: Parse HTML if API fails
    if hasattr(raw, 'text'):
        content = raw.text
    elif hasattr(raw, 'content'):
        content = raw.content.decode('utf-8')
    else:
        content = str(raw)
    
    # Parse HTML
    tree = lxml_html.fromstring(content)
    
    # Find hero items
    hero_items = tree.xpath('//div[contains(@class, "mt-list-item")]')
    
    for item in hero_items:
        img = item.xpath('.//img[contains(@alt, "hero")]')
        if not img:
            continue
        
        img = img[0]
        text_elements = item.xpath('.//div[contains(@class, "mt-text")]//text()')
        text_elements = [t.strip() for t in text_elements if t.strip()]
        
        if text_elements:
            name = text_elements[0]
            img_src = img.get('src') or img.get('data-src', '')
            heroid = str(len(heroes) + 1)
            
            id_match = re.search(r'homepage_(\d+_\d+_\d+)', img_src)
            if id_match:
                heroid = id_match.group(1).replace('_', '')
            
            heroes.append({
                "heroid": heroid,
                "channelid": "1",
                "name": name,
                "role": text_elements[1] if len(text_elements) > 1 else "Unknown"
            })
    
    return heroes


def parse_hero_detail(raw):
    # Parse API response
    data = None
    if hasattr(raw, 'json'):
        try:
            data = raw.json()
        except:
            pass
    elif isinstance(raw, dict):
        data = raw
    
    if data and isinstance(data, dict) and 'data' in data:
        data_obj = data.get('data', {})
        if isinstance(data_obj, dict) and 'records' in data_obj:
            records = data_obj['records']
            
            if records:
                record_data = records[0].get('data', {})
                return {
                    "name": "",  # Name already in heroes table
                    "role": "",  # Role already in heroes table
                    "specialty": [],
                    "difficulty": None,
                    "description": record_data.get('desc', '')
                }
    
    # Fallback: old format
    if data and isinstance(data, dict) and "data" in data:
        d = data["data"]
        if isinstance(d, dict):
            return {
                "name": d.get("name", ""),
                "role": d.get("role", ""),
                "specialty": d.get("specialty", []),
                "difficulty": d.get("difficulty"),
                "description": d.get("desc", "")
            }
    
    # Handle HTML response - return empty/default
    return {
        "name": "",
        "role": "",
        "specialty": [],
        "difficulty": None,
        "description": ""
    }


def parse_skills(raw):
    skills = []
    
    # Parse API response
    data = None
    if hasattr(raw, 'json'):
        try:
            data = raw.json()
        except:
            pass
    elif isinstance(raw, dict):
        data = raw
    
    if data and isinstance(data, dict) and 'data' in data:
        data_obj = data.get('data', {})
        if isinstance(data_obj, dict) and 'records' in data_obj:
            records = data_obj['records']
            
            for record in records:
                record_data = record.get('data', {})
                skill_ids = record_data.get('skill_id', [])
                
                for skill in skill_ids:
                    skill_data = skill.get('data', {})
                    skills.append({
                        "name": f"Skill {skill_data.get('skillid', '')}",
                        "type": "Active",
                        "cooldown": None,
                        "cost": None,
                        "desc": record_data.get('desc', '')  # General description
                    })
                
                # Only get from first record
                break
    
    # Fallback: old format
    if not skills and data and isinstance(data, dict) and "data" in data:
        data_inner = data.get("data", {})
        if isinstance(data_inner, dict) and "skills" in data_inner:
            for s in data_inner["skills"]:
                skills.append({
                    "name": s["name"],
                    "type": s["type"],
                    "cooldown": s.get("cooldown"),
                    "cost": s.get("cost"),
                    "desc": s["desc"]
                })
    
    return skills


def build_skill_combos(skills):
    ordered = [s["name"] for s in skills if s["type"] != "Passive"]
    if len(ordered) >= 3:
        return [ordered[:3]]
    return [ordered]
