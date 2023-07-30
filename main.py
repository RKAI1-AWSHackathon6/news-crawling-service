from utils import time_util, celery_util
from app import get_db, SessionLocal
from crawler import NewspapersCrawler
from multiprocessing import Pool
import db_crud
import logging
from pprint import pprint
import traceback
import schemas
from core.celery_app import celery_app
import time
import argparse
craw_args = argparse.ArgumentParser()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

crawler = NewspapersCrawler()
def crawl_new_articles_worker(newspaper_site):
        source_id = newspaper_site["source_id"]
        rss_url = newspaper_site["source_rss"]
        latest_published_timestamp = newspaper_site["latest_published_time"]
        try:
            articles = crawler.crawl_articles_rss(rss_url,latest_published_timestamp)
            logger.info(f"Number of articles crawled: {len(articles)} from {rss_url}")
        except Exception as e:
            logger.info(f"Error: {e} when crawling {rss_url}")
            traceback.print_exc()
        try:
            db = SessionLocal()
            for article in articles:
                try:
                    article["source_id"] = source_id
                    article["created_at"] = time_util.get_now_time_stamp()
                    logger.info(f"Added article title {article['title']}")
                    article_schema = schemas.ArticleBase(**article)
                    added_article = db_crud.create_article(db=db,article=article_schema)
                    logger.info("Sending article to worker")
                    added_id = added_article.id 
                    task_id = celery_app.send_task("app.worker.processing", args=[added_id])
                except Exception as e:
                    logger.info(f"Error: {e} when adding article {article['title']} ")
                    traceback.print_exc()
        finally:
            db.close()

def crawl_new_articles(limit=10):
    newspaper_site_info = []
    try:
        db = SessionLocal()
        newspaper_sites = db_crud.get_newspaper_site(db=db,limit=limit)
        # Find the latest publish time of the articles in the database for each newspaper site
        for newspaper in newspaper_sites:
            latest_publish_time = db_crud.get_latest_publish_time(db=db,source_id=newspaper.id)
            newspaper_site_info.append({"source_id":newspaper.id,"source_url": newspaper.source_url, "source_rss": newspaper.source_rss, "latest_published_time": latest_publish_time[0] if latest_publish_time else None})
    finally:
        db.close()

    with Pool(2) as p:
        results = p.map(crawl_new_articles_worker, newspaper_site_info)

def run_forever(sleep_time):
    while True:
        crawl_new_articles()
        time.sleep(60*10)

if __name__ == "__main__":
    craw_args.add_argument("--sleep_time",type=int,default=60*10)
    args = craw_args.parse_args()
    run_forever(args.sleep_time)
    
    