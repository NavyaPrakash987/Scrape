import praw
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load .env variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Initialize Reddit API (PRAW)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# ====== 📝 Your Keywords =======
keywords = ["NPCI", "UPI", "RuPay", "FASTag"]
# ===============================

def count_posts(keyword, subreddit="all"):
    """Counts number of Reddit posts where keyword is in title"""
    subreddit_obj = reddit.subreddit(subreddit)
    count = 0
    for submission in tqdm(subreddit_obj.search(keyword, sort='new', limit=None), desc=f"Counting posts for '{keyword}'"):
        if keyword.lower() in submission.title.lower():
            count += 1
    return count

def main():
    print("\n🔍 Counting Reddit posts for keywords (title only)...\n")
    results = {}

    for keyword in keywords:
        count = count_posts(keyword)
        results[keyword] = count

    print("\n📊 Summary:")
    print("-" * 30)
    for kw, cnt in results.items():
        print(f"Keyword: {kw:<10} | Posts Found (title match): {cnt}")
    print("-" * 30)

if __name__ == "__main__":
    main()
