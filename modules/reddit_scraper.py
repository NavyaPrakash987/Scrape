import praw
from newspaper import Article

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return e
    
def scrape_reddit(client_id, client_secret, user_agent, query="NPCI", subreddit="india", limit=50):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit.search(query, limit=limit):
        posts.append({"title": post.title, "score": post.score, "url": post.url, "selftext": post.selftext, "created": post.created_utc, "article_content" : extract_article_content(post.url) })
    return posts