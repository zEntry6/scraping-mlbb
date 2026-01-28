from patchright.sync_api import sync_playwright
import re
import json


class RankScraper:
    def __init__(self):
        pass

    def scrape(self):
        """Scrape rank data from rendered HTML page"""
        
        ranks = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto("https://www.mobilelegends.com/en/rank", wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(5000)
            
            # Wait for rank data to load
            try:
                page.wait_for_selector('[class*="rank"]', timeout=10000)
            except:
                pass
            
            # Extract all text content
            content = page.content()
            
            # Try to find hero data in page
            # Look for patterns like hero names followed by rates
            hero_elements = page.locator('[class*="hero"]').all()
            
            for i, el in enumerate(hero_elements[:100]):  # Limit to first 100
                try:
                    text = el.inner_text()
                    # Look for rates pattern: XX.XX%
                    rates = re.findall(r'(\d+\.\d+)%', text)
                    
                    if len(rates) >= 3:  # win, pick, ban rates
                        ranks.append({
                            "heroid": str(i+1),
                            "name": "",
                            "win_rate": float(rates[0]) / 100 if rates else 0,
                            "pick_rate": float(rates[1]) / 100 if len(rates) > 1 else 0,
                            "ban_rate": float(rates[2]) / 100 if len(rates) > 2 else 0,
                            "tier": None,
                            "counters": None
                        })
                except:
                    continue
            
            browser.close()
        
        return ranks if ranks else []
