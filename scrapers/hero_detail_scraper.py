from patchright.sync_api import sync_playwright
from parsers.hero_parser import build_skill_combos
import re


class HeroDetailScraper:
    def __init__(self):
        pass

    def scrape(self, heroid, channelid, hero_name=""):
        """Scrape hero details using browser automation with API interception for counter data"""
        
        url = f"https://www.mobilelegends.com/en/hero/detail?channelid={channelid}&heroid={heroid}"
        
        # Storage for API data
        counter_data = None
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Intercept API response for counter data (endpoint 2756564)
            def handle_response(response):
                nonlocal counter_data
                if '2756564' in response.url:  # Counter/relation data endpoint
                    try:
                        data = response.json()
                        if data.get('code') == 0 and 'data' in data:
                            records = data['data'].get('records', [])
                            for record in records:
                                if record.get('data', {}).get('hero_id') == heroid:
                                    counter_data = record['data'].get('relation', {})
                                    break
                    except:
                        pass
            
            page.on("response", handle_response)
            
            # Load hero detail page
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(4000)  # Wait for content to load
            
            # Scroll down to trigger lazy-loading of all content
            try:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(3000)  # Wait longer for API calls
                page.evaluate("window.scrollTo(0, 0)")  # Scroll back to top
                page.wait_for_timeout(1000)
            except:
                pass
            
            # Extract hero name from page if not provided
            if not hero_name:
                try:
                    # Try to get hero name from page title or h1
                    hero_name_element = page.locator('h1, [class*="hero-name"]').first
                    hero_name = hero_name_element.inner_text(timeout=2000)
                    hero_name = hero_name.strip()
                except:
                    pass
            
            # Extract win/pick/ban rates from page
            win_rate = 0.0
            pick_rate = 0.0
            ban_rate = 0.0
            
            try:
                # Look for rate text like "50.25%"
                html = page.content()
                rate_pattern = re.compile(r'(\d+\.\d+)%')
                rates = rate_pattern.findall(html)
                
                # Usually the first 3 percentage values are win/pick/ban rates
                if len(rates) >= 3:
                    win_rate = float(rates[0]) / 100
                    pick_rate = float(rates[1]) / 100
                    ban_rate = float(rates[2]) / 100
            except:
                pass
            
            # Extract counter information from API data OR page content
            counter_info = {
                "counters": "",  # Meng-Counter (strong against)
                "countered_by": "",  # Di-Counter oleh (weak against)
                "synergy": ""  # Kecocokan (works well with/assist)
            }
            
            # Try API data first (for newer heroes)
            if counter_data:
                try:
                    # Extract "strong" = Meng-Counter (heroes this hero counters)
                    if 'strong' in counter_data:
                        strong = counter_data['strong']
                        counter_info["counters"] = strong.get('desc', '')[:500]
                    
                    # Extract "weak" = Di-Counter oleh (heroes that counter this hero)
                    if 'weak' in counter_data:
                        weak = counter_data['weak']
                        counter_info["countered_by"] = weak.get('desc', '')[:500]
                    
                    # Extract "assist" = Kecocokan (heroes that work well with this hero)
                    if 'assist' in counter_data:
                        assist = counter_data['assist']
                        counter_info["synergy"] = assist.get('desc', '')[:500]
                except Exception as e:
                    print(f"Error parsing counter data: {e}")
            
            # If no API data, try to extract from page HTML
            if not counter_info["counters"]:
                try:
                    html = page.content()
                    
                    # Pattern: Find text after "Meng-Counter", "Di-Counter oleh", "Kecocokan" headers
                    # Looking for span elements with hero name in text (indicating counter description)
                    
                    # Find Meng-Counter section
                    meng_match = re.search(
                        r'Meng-Counter.*?<span[^>]*>([^<]*' + re.escape(hero_name) + r'[^<]{50,400})</span>',
                        html, re.DOTALL | re.IGNORECASE
                    )
                    if meng_match:
                        counter_info["counters"] = meng_match.group(1).strip()[:500]
                    
                    # Find Di-Counter section  
                    dicounter_match = re.search(
                        r'Di-Counter.*?<span[^>]*>([^<]*' + re.escape(hero_name) + r'[^<]{50,400})</span>',
                        html, re.DOTALL | re.IGNORECASE
                    )
                    if dicounter_match:
                        counter_info["countered_by"] = dicounter_match.group(1).strip()[:500]
                    
                    # Find Kecocokan section
                    kecocokan_match = re.search(
                        r'Kecocokan.*?<span[^>]*>([^<]*' + re.escape(hero_name) + r'[^<]{50,400})</span>',
                        html, re.DOTALL | re.IGNORECASE
                    )
                    if kecocokan_match:
                        counter_info["synergy"] = kecocokan_match.group(1).strip()[:500]
                        
                except Exception as e:
                    pass  # Counter section might not exist
            
            # Extract skills from HTML
            skills = []
            try:
                # Find all skill blocks using regex
                # Pattern: <span>Skill Name</span> followed by <div class="mt-rich-text-content">description</div>
                skill_pattern = re.compile(
                    r'<span[^>]*>([^<]+)</span>.*?<div class="mt-rich-text-content">(.+?)</div>',
                    re.DOTALL
                )
                
                matches = skill_pattern.findall(html)
                
                for name, desc_html in matches:
                    name = name.strip()
                    # Remove HTML tags from description
                    desc = re.sub(r'<[^>]+>', '', desc_html)
                    desc = desc.strip()
                    
                    # Filter out non-skill content
                    # Skip if name is just numbers (timestamp) or too short
                    if name.isdigit() or len(name) < 4 or len(name) > 50:
                        continue
                    
                    # Skip if description is too short
                    if len(desc) < 30:
                        continue
                    
                    # Check if it looks like a skill (contains damage, effect keywords)
                    skill_keywords = ['damage', 'cooldown', 'effect', 'skill', 'attack', 'hp', 'strikes', 'deals', 'physical', 'magic', 'enemy', 'target', 'hero', 'cd', 'mana']
                    if not any(keyword in desc.lower() for keyword in skill_keywords):
                        continue
                    
                    # OPTIONAL FILTER: If hero name provided, prefer skills with hero name but don't skip others
                    # This helps prioritize correct skills but doesn't exclude generic skill descriptions
                    has_hero_name = hero_name and hero_name.lower() in desc.lower()
                    
                    skills.append({
                        "name": name,
                        "type": "Passive" if "passive" in name.lower() else "Active",
                        "cooldown": None,
                        "cost": None,
                        "desc": desc[:500],  # Limit description length
                        "priority": 1 if has_hero_name else 0  # For sorting if needed
                    })
                
                # Sort by priority (skills with hero name first) and limit to reasonable number
                skills.sort(key=lambda x: x.get('priority', 0), reverse=True)
                skills = skills[:6]  # Max 6 skills per hero (passive + 4 actives + ult)
                
            except Exception as e:
                print(f"Error extracting skills: {e}")
            
            browser.close()
        
        combos = build_skill_combos(skills)
        
        return {
            "hero": {"name": "", "role": "", "specialty": [], "difficulty": None, "description": ""},
            "skills": skills,
            "combos": combos,
            "rates": {
                "win_rate": win_rate,
                "pick_rate": pick_rate,
                "ban_rate": ban_rate
            },
            "counter_info": counter_info
        }
