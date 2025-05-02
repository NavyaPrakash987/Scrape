import feedparser

def fetch_rss_news(feed_url="https://www.livemint.com/rss/companies" ):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({"title": entry.title, "link": entry.link, "published": entry.published})
    return articles