from fetchers.hero_fetcher import HeroFetcher
from parsers.hero_parser import parse_hero_list


class HeroListScraper:
    def __init__(self):
        self.fetcher = HeroFetcher()

    def scrape(self):
        raw = self.fetcher.fetch_hero_list()
        return parse_hero_list(raw)
