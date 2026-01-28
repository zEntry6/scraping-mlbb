from storage.db import init_db
from storage.hero_repo import upsert_heroes, save_hero_detail
from storage.rank_repo import save_rank_snapshot

from scrapers.hero_list_scraper import HeroListScraper
from scrapers.hero_detail_scraper import HeroDetailScraper
from scrapers.rank_scraper import RankScraper


def main():
    init_db()

    print("Scraping hero list...")
    hero_list = HeroListScraper().scrape()
    print(f"Found {len(hero_list)} heroes")
    upsert_heroes(hero_list)

    print("\nScraping hero details...")
    detail_scraper = HeroDetailScraper()
    for i, hero in enumerate(hero_list):
        print(f"  {i+1}/{len(hero_list)}: {hero['name']}")
        detail = detail_scraper.scrape(
            hero["heroid"],
            hero["channelid"],
            hero["name"]  # Pass hero name for skill filtering
        )
        save_hero_detail(hero["heroid"], detail)  # Pass full detail object

    print("\nScraping rankings...")
    ranks = RankScraper().scrape()
    print(f"Found {len(ranks)} ranked heroes")
    save_rank_snapshot(ranks)
    
    print("\nScraping completed!")


if __name__ == "__main__":
    main()
