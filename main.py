import json
import os
from modules import *
import logging
# from modules.reddit_scraper import scrape_reddit
# from modules.rss_monitor import fetch_rss_news
# from modules.twitter_scraper import scrape_twitter
# from modules.vector_store import build_vector_store, query_vector_store
# from modules.website_crawler import crawl_website
# from dotenv import  load_dotenv
from modules.request_utils import save_json
from modules.reddit_scraper import init_reddit, scrape_keyword
from psaw import PushshiftAPI
import config


# ---- Configure Logging ----
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if not os.path.exists('data/reddit'):
    os.makedirs('data/reddit')


reddit = init_reddit(config.REDDIT_CLIENT_ID, config.REDDIT_CLIENT_SECRET, config.REDDIT_USER_AGENT)

for keyword in config.KEYWORDS:
   
    results = scrape_keyword(reddit, keyword,limit=1000, subreddit_name='all')
    save_json(results, f"data/reddit/{keyword}_reddit_data.json")
    print(f"✅ Saved {len(results)} posts for '{keyword}' to data/reddit/{keyword}_reddit_data.json")

logging.info("Scraping complete ✅")

# Crawl NPCI site
# site_data = crawl_website("https://www.npci.org.in", max_pages=30)
# logger.info("crawl NPCI site")
# with open("data/npc_site_data.json", "w") as f:
#     json.dump(site_data, f, indent=2)



# # Fetch RSS articles
# rss_articles = fetch_rss_news()
# with open("data/news_articles.json", "w") as f:
#     json.dump(rss_articles, f, indent=2)

# # Build vector store and search
# build_vector_store(site_data)
# results = query_vector_store("UPI transactions in India")
# for r in results:
#     print("Result\n", r[0][:300], "...\n")

# # Scrape Twitter
# tweets_df = scrape_twitter("NPCI OR RuPay OR UPI")
# tweets_df.to_csv("data/npc_tweets.csv", index=False)