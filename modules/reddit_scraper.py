# modules/reddit_scraper.py
import praw
from praw.models import MoreComments
from newspaper import Article
from tqdm import tqdm

def init_reddit(client_id, client_secret, user_agent):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    return reddit

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception:
        return ""

def fetch_comments(submission):
    submission.comments.replace_more(limit=None)
    comments_data = []

    def extract_comment(comment):
        return {
            "id": comment.id,
            "author": str(comment.author),
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "replies": [extract_comment(reply) for reply in comment.replies]
        }

    for top_level_comment in submission.comments:
        comments_data.append(extract_comment(top_level_comment))

    return comments_data

def is_relevant_post(submission, keyword):
    """Check if keyword is explicitly in title or selftext"""
    text = f"{submission.title}".lower()
    return keyword.lower() in text

def scrape_keyword(reddit, keyword, limit=1000, subreddit_name='all'):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    print(f"\n🔍 Scraping keyword: {keyword} in r/{subreddit_name}")

    for submission in tqdm(subreddit.search(query=keyword, sort='new', limit=limit), desc=f"Fetching posts for '{keyword}'"):
        if is_relevant_post(submission, keyword):  # <-- Add explicit check here
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "url": submission.url,
                "created_utc": submission.created_utc,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "subreddit": submission.subreddit.display_name,
                "author": str(submission.author),
                "article_content": extract_article_content(submission.url) if submission.url.startswith('http') else "",
                "comments": fetch_comments(submission)
            }
            posts.append(post_data)

    return posts
