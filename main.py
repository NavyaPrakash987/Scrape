import json
import os
from modules import *
import logging
from modules.reddit_scraper import scrape_reddit
from modules.rss_monitor import fetch_rss_news
from modules.twitter_scraper import scrape_twitter
from modules.vector_store import build_vector_store, query_vector_store
from modules.website_crawler import crawl_website
from dotenv import  load_dotenv

load_dotenv()
if not os.path.exists("data"):
    os.mkdir("data")

# ---- Configure Logging ----
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Crawl NPCI site
# site_data = crawl_website("https://www.npci.org.in", max_pages=30)
# logger.info("crawl NPCI site")
# with open("data/npc_site_data.json", "w") as f:
#     json.dump(site_data, f, indent=2)

reddit_id = os.getenv("reddit_id")
reddit_secret = os.getenv("reddit_secret")
reddit_user_agent = os.getenv("reddit")

# print(reddit_id , reddit_secret , reddit) 
# # Scrape Reddit
# reddit_posts = scrape_reddit(reddit_id, reddit_secret, reddit)
# with open("data/reddit_posts.json", "w") as f:
#     json.dump(reddit_posts, f, indent=2)

if not all([reddit_id, reddit_secret, reddit_user_agent]):
    logging.error("One or more Reddit credentials are missing. Check your .env file.")
    exit(1)

logging.info(f"Reddit client_id loaded: {reddit_id}")
logging.info(f"Reddit user_agent loaded: {reddit_user_agent}")

# ---- Create data directory if not exists ----
if not os.path.exists("data"):
    os.mkdir("data")
    logging.info("Created 'data' directory")
else:
    logging.info("'data' directory already exists")

# ---- Scrape Reddit ----
logging.info("Starting Reddit scrape...")
try:
    reddit_posts = scrape_reddit(reddit_id, reddit_secret, reddit_user_agent)
    logging.info(f"Scraped {len(reddit_posts)} posts from Reddit successfully")
except Exception as e:
    logging.error(f"Error during Reddit scraping: {e}")
    exit(1)

# ---- Save scraped posts ----
output_file = "data/reddit_posts.json"
try:
    with open(output_file, "w") as f:
        json.dump(reddit_posts, f, indent=2)
    logging.info(f"Saved scraped posts to '{output_file}'")
except Exception as e:
    logging.error(f"Error saving scraped posts: {e}")
    exit(1)

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