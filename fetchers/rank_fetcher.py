from fetchers.base_fetcher import BaseFetcher
from config.settings import RANK_API
from utils.logger import get_logger
import time
import random
import json
import subprocess
import tempfile
import os

logger = get_logger()

class RankFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(use_browser=False)
    
    def fetch_rankings(self):
        time.sleep(random.uniform(3, 5))
        
        logger.info("Fetching rank data from browser automation")
        
        # Create a temporary script to run browser automation in subprocess
        script = '''
from patchright.sync_api import sync_playwright
import json

rank_data = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    def handle_response(response):
        global rank_data
        if '2756567' in response.url and response.status == 200:
            try:
                rank_data = response.json()
            except:
                pass
    
    page.on("response", handle_response)
    page.goto("https://www.mobilelegends.com/en/rank", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    browser.close()

if rank_data:
    print(json.dumps(rank_data))
'''
        
        # Write script to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_script = f.name
        
        try:
            # Run script in subprocess
            result = subprocess.run(
                ['py', temp_script],
                capture_output=True,
                text=True,
                timeout=90
            )
            
            if result.returncode == 0 and result.stdout:
                rank_data = json.loads(result.stdout)
                return rank_data
            else:
                raise Exception(f"Failed to fetch rank data: {result.stderr}")
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_script)
            except:
                pass
