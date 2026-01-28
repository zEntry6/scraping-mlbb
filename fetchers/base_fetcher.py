from utils.logger import get_logger
import httpx
from patchright.sync_api import sync_playwright
import time

logger = get_logger()

_playwright_instance = None
_browser_instance = None

def get_browser():
    global _playwright_instance, _browser_instance
    if _browser_instance is None:
        _playwright_instance = sync_playwright().start()
        _browser_instance = _playwright_instance.chromium.launch(headless=True)
    return _browser_instance

class BaseFetcher:
    def __init__(self, use_browser=True):
        self.use_browser = use_browser
        self.client = httpx.Client(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=30.0
        )
        
        if use_browser:
            try:
                self.browser = get_browser()
            except Exception as e:
                logger.warning(f"Failed to init browser: {e}, falling back to httpx")
                self.use_browser = False

    def get(self, url: str):
        logger.info(f"Fetching: {url}")
        try:
            if self.use_browser and self.browser:
                page = self.browser.new_page()
                try:
                    page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    time.sleep(5)  # Wait for JS to execute
                    content = page.content()
                    page.close()
                    
                    # Return a mock response object with text property
                    class BrowserResponse:
                        def __init__(self, html, url):
                            self.text = html
                            self.url = url
                            self.status_code = 200
                    
                    return BrowserResponse(content, url)
                except Exception as e:
                    page.close()
                    raise e
            else:
                response = self.client.get(url)
                response.raise_for_status()
                return response
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            # Fallback to httpx if browser fails
            if self.use_browser:
                logger.info("Browser fetch failed, trying with httpx...")
                self.use_browser = False
                response = self.client.get(url)
                response.raise_for_status()
                return response
            raise
    
    def close(self):
        # Don't close browser as it's shared
        pass
