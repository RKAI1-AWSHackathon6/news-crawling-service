import requests

newspaper_website =[
    "https://cryptobriefing.com/",
    "https://www.coindesk.com/",
    "https://www.cryptodaily.co.uk",
    "https://cointelegraph.com/",
    "https://blog.bitmex.com"
    
]

newspaper_rss = [
    "https://cryptobriefing.com/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss",
    "https://www.cryptodaily.co.uk/feed",
    "https://cointelegraph.com/rss",
    "https://blog.bitfinex.com/feed",
    "https://blog.bitmex.com/feed/",
    "https://www.forbes.com/crypto-blockchain/feed/",
    "https://www.investing.com/rss/news_301.rss"
]
newspaper_db = {
    "https://cryptobriefing.com/": "https://cryptobriefing.com/feed",
    "https://www.coindesk.com/": "https://www.coindesk.com/arc/outboundfeeds/rss",
    "https://www.cryptodaily.co.uk": "https://www.cryptodaily.co.uk/feed",
    "https://cointelegraph.com/": "https://cointelegraph.com/rss",
    "https://www.forbes.com/crypto-blockchain/": "https://www.forbes.com/crypto-blockchain/feed",
    "https://www.investing.com/": "https://www.investing.com/rss/news_301.rss",
    "https://www.coinspeaker.com/news": "https://www.coinspeaker.com/news/feed",
    "https://crypto.news":"https://crypto.news/feed",
    "https://thecryptotime.com":"https://thecryptotime.com/feed",
    "https://cryptoslate.com":"https://cryptoslate.com/feed",
    "https://blog.bitmex.com":"https://blog.bitmex.com/feed",
    "https://coingeek.com/":"https://coingeek.com/feed",
}

def add_newspaper_site_test():
    url = "http://10.1.38.150:9995/api/v1/newspaper/add"
    body = {"source_url": "https://cryptobriefing.com/", "source_rss": "https://cryptobriefing.com/feed"}
    response = requests.post(url, json=body)
    print(response.json())
    
def add_newspaper_site():
    url = "http://10.1.38.150:9995/api/v1/newspaper/add"
    for newspaper in newspaper_db:
        body = {"source_url": newspaper, "source_rss": newspaper_db[newspaper]}
        response = requests.post(url, json=body)
        print(response.json())

if __name__ == "__main__":
    add_newspaper_site()
    