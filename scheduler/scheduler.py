from apscheduler.schedulers.blocking import BlockingScheduler
from scrapers.rank_scraper import RankScraper
from analysis.meta_analysis import analyze_meta

scheduler = BlockingScheduler()

def daily_rank_job():
    rankings = RankScraper().scrape()
    meta = analyze_meta(rankings)
    print("Daily meta snapshot collected")

scheduler.add_job(daily_rank_job, "interval", days=1)

def start():
    scheduler.start()
