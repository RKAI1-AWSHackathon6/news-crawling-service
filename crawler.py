import newspaper
from newspaper import Config
import xml.etree.ElementTree as ET
from pprint import pprint
import urllib.request
import sys
from datetime import datetime
import logging
from core.celery_app import celery_app
from utils import celery_util, time_util
import dateutil.parser as datetime_parser
from trafilatura import fetch_url, extract
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


del_sentence = "Share this article URL Copied\n"
newspaper_rss = [
    "https://cryptobriefing.com/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss",
    "https://www.cryptodaily.co.uk/feed",
    "https://cointelegraph.com/rss",
    "https://blog.bitfinex.com/feed",
    "https://blog.bitmex.com/feed/",
    "https://www.forbes.com/crypto-blockchain/feed/",
    "https://www.investing.com/rss/news.rss",
    "https://www.investing.com/rss/news_301.rss"
]

newspaper_rss_test = [
    "https://cryptobriefing.com/feed",
]

headers = {'User-Agent': 'Mozilla/5.0'} 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

class CrawlerUtils:
    @classmethod
    def get_articles_from_rss(cls,url):
        req_site = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            rss = urllib.request.urlopen(req_site).read()
        except Exception as e:
            print(e)
            with urllib.request.urlopen(url) as response:
                rss = response.read()
        xml_tree = ET.ElementTree(ET.fromstring(rss))
        # Get the root element
        root = xml_tree.getroot()
        news_items = []
        for item in root.findall("channel/item"):
            news_item = {}
            for child in item:
                if child.tag == "title":
                    news_item["title"] = child.text
                elif child.tag == "link":
                    news_item["origin_link"] = child.text
                elif child.tag == "description":
                    news_item["description"] = child.text
                elif child.tag == "pubDate":
                    try:
                        # date_obj = datetime.strptime(child.text, "%a, %d %b %Y %H:%M:%S %z")
                        date_obj = datetime_parser.parse(child.text)
                        news_item["published_timestamp"] = int(date_obj.timestamp())
                    except Exception as e:
                        logger.error(f"Unable to format datetime string {child.text}")
                        continue
                elif child.attrib.get("medium",None) == "image" or child.attrib.get("type",None) == "image/jpeg" :
                    news_item["thumbnail_image_link"] = child.attrib["url"]
            news_items.append(news_item)
        return news_items

    @classmethod
    def get_article_content(cls,url):
        """Get Article Content"""
        article = newspaper.Article(url,config=config)
        article.download()
        article.parse()
        downloaded = fetch_url(url)
        result = extract(downloaded)
        return result, article.authors, article.images

    
class NewspapersCrawler:
    def __init__(self):
        pass

    def crawl_articles_rss(self,rss_url, latest_published_date, kw_extraction=True):
        return_articles = []
        logger.info(f"Crawling {rss_url}")
        articles = CrawlerUtils.get_articles_from_rss(rss_url)
        logger.info(f"Number of articles crawled: {len(articles)}")
        for article in articles:
            if latest_published_date is not None:
                current_article_pub_date_timestamp = article["published_timestamp"] 
                if current_article_pub_date_timestamp <= latest_published_date:
                    logger.info("Article published date is older than the latest published date in the database")
                    continue
            url_link = article["origin_link"]
            try:
                article_content, article_authors, article_images = CrawlerUtils.get_article_content(url_link)
            except Exception as e:
                logger.error(f"Error: {e} when crawling {url_link}")
                continue
            article["author"] = ",".join(article_authors) if len(article_authors) > 0 else ""
            article["body_image"] = ",".join(article_images)
            if del_sentence in article_content:
                del_sentence_pos = article_content.find(del_sentence)
                article_content = article_content[del_sentence_pos + len(del_sentence):]
                article_content = article_content[1:] if article_content[0] == "\n" else article_content
            article["body"] = str(article_content)
            # If need to extract tag from content
            if kw_extraction:
                logger.info("Extracting keywords")
                task_id = celery_app.send_task("worker.keyword_extraction", args=[article_content])
                status,kws_result = celery_util.get_task_result(task_id)
                if status == True:
                    kws_status, kws = kws_result
                    article["tag"] = ",".join(list(kws)) if len(list(kws)) > 0 else ""
                else:
                    article["tag"] = ""
            return_articles.append(article)
        return return_articles
        
if __name__ == "__main__":
    crawler = NewspapersCrawler()
    crawler.crawl_articles_rss(newspaper_rss_test[0],None, kw_extraction=True)