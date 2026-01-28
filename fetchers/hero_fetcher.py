from fetchers.base_fetcher import BaseFetcher
from config.settings import BASE_URL, HERO_LIST_API
from config.constants import HERO_DETAIL_PATH
from utils.logger import get_logger
import time
import random

logger = get_logger()

class HeroFetcher(BaseFetcher):
    def __init__(self):
        # Use httpx for API calls, not browser
        super().__init__(use_browser=False)
        
        # Update headers for API requests
        self.client.headers.update({
            'x-actid': '2669607',
            'authorization': 'CciHBEvFRqQNHGj2djxdUSja7W4=',
            'referer': 'https://www.mobilelegends.com/',
            'x-lang': 'en',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'x-appid': '2669606'
        })
    
    def fetch_hero_list(self):
        time.sleep(random.uniform(2, 4))
        
        # API requires POST with specific payload
        payload = {
            "pageSize": 200,  # Get all heroes
            "pageIndex": 1,
            "filters": [
                {"field": "<hero.data.sortid>", "operator": "hasAnyOf", "value": [1,2,3,4,5,6]},
                {"field": "<hero.data.roadsort>", "operator": "hasAnyOf", "value": [1,2,3,4,5]}
            ],
            "sorts": [{"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}],
            "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
            "object": []
        }
        
        logger.info(f"Fetching hero list from API: {HERO_LIST_API}")
        response = self.client.post(HERO_LIST_API, json=payload)
        response.raise_for_status()
        return response

    def fetch_hero_detail(self, heroid, channelid):
        time.sleep(random.uniform(2, 4))
        
        # Use API for hero detail
        from config.settings import HERO_DETAIL_API
        
        payload = {
            "pageSize": 10,
            "pageIndex": 1,
            "filters": [{"field": "data.hero_id", "operator": "=", "value": int(heroid)}],
            "sorts": [],
            "fields": ["data.hero_id", "data.desc", "data.skill_id"],
            "object": []
        }
        
        logger.info(f"Fetching hero detail for heroid={heroid} from API")
        response = self.client.post(HERO_DETAIL_API, json=payload)
        response.raise_for_status()
        return response
