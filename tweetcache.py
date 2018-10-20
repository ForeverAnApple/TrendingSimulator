import sqlite3
import time
from datetime import datetime


class TweetCache:
    def __init__(self, cache_db="TweetCache.db"):
        self.db = sqlite3.connect(cache_db)

        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tweet (
            tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            body TEXT NOT NULL,
            hashtag TEXT NOT NULL,
            timestamp_added INTEGER NOT NULL)''')
        self.db.commit()

    # returns a tuple of (tweet_text, access_datetime)
    def get_tweets(self, hashtag):
        cursor = self.db.cursor()
        cursor.execute('SELECT body, timestamp_added FROM tweet t WHERE hashtag = ?', (hashtag,))

        for row in cursor:
            yield row[0], datetime.fromtimestamp(row[1])

    def add_tweet(self, body, hashtag, timestamp_added=int(time.time())):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO tweet (body, hashtag, timestamp_added) VALUES (?, ?, ?)',
                       (body, hashtag, timestamp_added))
        self.db.commit()


cache = TweetCache()
cache.add_tweet("This is a fake tweet", "Trending A")

print("Tweets in cache:")
for tweet in cache.get_tweets("Trending A"):
    print(tweet)
