import snscrape.modules.twitter as sntwitter
import pandas as pd

def scrape_twitter(query="NPCI", max_tweets=100):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append({"date": tweet.date, "content": tweet.content, "username": tweet.user.username})
    df = pd.DataFrame(tweets)
    return df