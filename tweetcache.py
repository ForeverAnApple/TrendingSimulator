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
        cursor.execute('''CREATE TABLE IF NOT EXISTS topic (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tweet (
            tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            body TEXT NOT NULL,
            topic_id INTEGER NOT NULL REFERENCES topic(topic_id),
            timestamp_added INTEGER NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS image (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL REFERENCES topic(topic_id),
            url TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS image_tag (
            image_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id INTEGER NOT NULL REFERENCES image(image_id),
            tag TEXT NOT NULL)''')
        self.db.commit()

    # returns a tuple of (tweet_text, access_datetime)
    def get_tweets(self, topic):
        cursor = self.db.cursor()
        cursor.execute('SELECT body, timestamp_added FROM tweet t WHERE topic = ?', (topic,))

        for row in cursor:
            yield row[0], datetime.fromtimestamp(row[1])

    def add_tweets(self, tweets, topic):
        cursor = self.db.cursor()
        for tweet in tweets:
            cursor.execute('INSERT INTO tweet (body, topic, timestamp_added) VALUES (?, ?, ?)',
                           (tweet.text, topic, int(time.time())))
            print((tweet.text, topic))
        self.db.commit()
