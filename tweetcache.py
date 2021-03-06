import sqlite3
import time
import os, errno
from cloudvision import VisionApi
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

    # Find all images that needs tagging
    def get_notag_images(self, topic):
        cursor = self.db.cursor()
        cursor.execute('''SELECT image.image_id, image.url
            FROM image
            JOIN topic ON image.topic_id = topic.topic_id
            WHERE (SELECT COUNT(*) FROM image_tag WHERE image_tag.image_id = image.image_id) = 0
            AND topic_name = ?''', (topic,))
        return cursor

    def add_image_tags(self, images, topic):
        img_i = 0
        image_tags = list()
        img_req = list()
        for image in images:
            img_req.append((image[0], image[1]))
            img_i += 1
            # Every 16 images in the request the google vision api will run, returning all the labels generated for all
            # the images with their image id
            if img_i == 16:
                vision = VisionApi(img_req)
                labels = vision.getlabels(topic)
                for label in labels:
                    image_tags.append(label)
                img_i = 0
                img_req.clear()

        # Finish up the rest of the requests if needed.
        if len(img_req) != 0:
            vision = VisionApi(img_req)
            labels = vision.getlabels(topic)
            for label in labels:
                image_tags.append(label)

        print("image tags:", image_tags)
        # Now, add all these labels back into the database
        cursor = self.db.cursor()
        for image_tag in image_tags:
            for tag in image_tag[1]:
                cursor.execute('''INSERT INTO image_tag
                    (image_id, tag)
                    VALUES (?,?)
                ''', (image_tag[0], tag))
            self.db.commit()

    def get_images_for_word(self, word, topic):
        cursor = self.db.cursor()
        cursor.execute("""SELECT image.url
            FROM image
            JOIN image_tag ON image.image_id = image_tag.image_id
            JOIN topic ON image.topic_id = topic.topic_id
            WHERE (tag LIKE '% ' || ?
            OR tag LIKE '% ' || ? || ' %'
            OR tag LIKE ? || ' %'
            OR tag = ?)
            AND topic_name = ?""", (word, word, word, word, topic))
        for row in cursor:
            yield row[0]

    def get_images_for_topic(self, topic):
        cursor = self.db.cursor()
        cursor.execute('''SELECT image.url
            FROM image
            JOIN topic ON image.topic_id = topic.topic_id
            WHERE topic.topic_name LIKE ?''', (topic,))
        for row in cursor:
            yield row[0]

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
                FROM topic WHERE topic_name = ?''', (tweet, int(time.time()), topic))
        self.db.commit()

    def add_images(self, image_urls, topic):
        self.__add_topic(topic)
        cursor = self.db.cursor()
        for url in image_urls:
            cursor.execute('''INSERT INTO image (url, topic_id) SELECT ?, topic_id
                FROM topic WHERE topic_name = ?''', (url, topic))
        self.db.commit()


if __name__ == '__main__':
    cache = TweetCache()
    for x in cache.get_images_for_word("dog"):
        print(x)