import sqlite3
import time
import os, errno
from datetime import datetime


class TweetCache:
    def __init__(self, cache_db="var/TweetCache.db"):
        try:
            os.mkdir("var")
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise

        self.db = sqlite3.connect(cache_db)

        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tweet (
            tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            body TEXT NOT NULL,
            topic TEXT NOT NULL,
            timestamp_added INTEGER NOT NULL)''')
        self.db.commit()

    # returns a tuple of (tweet_text, access_datetime)
    def get_tweets(self, topic):
        cursor = self.db.cursor()
        cursor.execute('SELECT body, timestamp_added FROM tweet t WHERE topic = ?', (topic,))

        for row in cursor:
            yield row[0], datetime.fromtimestamp(row[1])

    def add_tweet(self, body, topic, timestamp_added=int(time.time())):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO tweet (body, topic, timestamp_added) VALUES (?, ?, ?)',
                       (body, topic, timestamp_added))
        self.db.commit()


cache = TweetCache()
cache.add_tweet("This is a fake tweet", "Trending A")

print("Tweets in cache:")
for tweet in cache.get_tweets("Trending A"):
    print(tweet)
