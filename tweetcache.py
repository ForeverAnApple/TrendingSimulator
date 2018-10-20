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

    # returns cache age in seconds
    def cache_age(self, topic):
        cursor = self.db.cursor()
        cursor.execute('''SELECT MAX(timestamp_added)
            FROM tweet
            JOIN topic ON tweet.topic_id = topic.topic_id
            WHERE topic_name = ?''', (topic,))
        latest_timestamp = cursor.fetchone()[0]
        if latest_timestamp is None:
            latest_timestamp = float('-inf')
        return int(time.time()) - latest_timestamp

    def get_tweets(self, topic):
        cursor = self.db.cursor()
        cursor.execute('''SELECT body
            FROM tweet 
            JOIN topic ON tweet.topic_id = topic.topic_id
            WHERE topic_name = ?''', (topic,))
        for row in cursor:
            yield row[0]

    # No-op if topic already exists
    def __add_topic(self, topic):
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(*) FROM topic WHERE topic_name = ?', (topic,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO topic (topic_name) VALUES (?)', (topic,))
            self.db.commit()

    def add_tweets(self, tweets, topic):
        self.__add_topic(topic)
        cursor = self.db.cursor()
        for tweet in tweets:
            cursor.execute('''INSERT INTO tweet (body, topic_id, timestamp_added) SELECT ?, topic_id, ?
                FROM topic where topic_name = ?''',
                           (tweet, int(time.time()), topic))
        self.db.commit()
