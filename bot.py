from selenium import webdriver
from urllib import request
import os
import random
import time
import re


class Bot:
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.trending_dictionary = {}
        self.trending_elements_names = []
        self.tweets = []
        self.formatted_tweets = []
        self.image_urls = []
        self.temp_file = None

    def navigate(self, url):
        self.browser.get(url)

    @staticmethod
    def sleep_range(min, max):
        time.sleep(random.uniform(min, max))

    @staticmethod
    def click_on_element(element_to_click):
        element_to_click.click()

    def slow_send_keys(self, field, text):
        for c in text:
            field.send_keys(c)
            self.sleep_range(0.01, 0.2)

    def login(self, username, password):
        # Navigate to the login page
        self.navigate('https://twitter.com/login')
        # Sleep for random amount of time
        self.sleep_range(1, 3)
        # Click the username field
        username_field = self.browser.find_element_by_class_name('js-username-field')
        self.slow_send_keys(username_field, username)
        self.sleep_range(1, 3)
        # Click the password field
        password_field = self.browser.find_element_by_class_name('js-password-field')
        self.slow_send_keys(password_field, password)
        self.sleep_range(1, 3)
        # Click the Log in button
        login_button = self.browser.find_element_by_class_name('submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
        login_button.click()
        self.sleep_range(1, 3)

    def send_tweet(self, tweet_to_send, attach_image):
        # Navigate to twitter home page
        self.navigate('https://twitter.com/')
        self.browser.implicitly_wait(5)

        if attach_image:
            # Post the Image
            input_class = self.browser.find_element_by_class_name('file-input.js-tooltip')
            self.browser.execute_script("arguments[0].type = 'file';", input_class)
            self.sleep_range(1,3)
            input_class.send_keys(r'%s' % os.path.join(os.getcwd(), 'tmpImage.jpg'))

        self.sleep_range(3, 5)

        # Select the field to make it expand
        tweet_field = self.browser.find_element_by_id('tweet-box-home-timeline')
        tweet_field.click()
        self.browser.implicitly_wait(5)
        # select the field to type into it
        tweet_field = self.browser.find_element_by_id('tweet-box-home-timeline')
        # tweet_field.click()
        self.sleep_range(3, 5)
        self.slow_send_keys(tweet_field, tweet_to_send)
        tweet_field.click()
        self.sleep_range(3, 5)

        # Click the tweet button
        #tweet_button = self.browser.find_element_by_class_name('tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
        #tweet_button.click()

    def select_trending_topics(self):
        # Clear the trending list
        self.trending_dictionary = {}
        # Implicitly wait for trending side bar
        self.browser.implicitly_wait(5)
        # Navigate to twitter home page
        self.navigate('https://twitter.com/')
        # Select trending hashtags parent
        trending_elements = self.browser.find_elements_by_class_name('pretty-link.js-nav.js-tooltip.u-linkComplex')
        self.trending_elements_names = self.browser.find_elements_by_class_name('u-linkComplex-target.trend-name')
        for x in range(len(trending_elements)):
            self.trending_dictionary[self.trending_elements_names[x]] = trending_elements[x]

        self.browser.implicitly_wait(10)

    @staticmethod
    def current_time_millis():
        return int(round(time.time() * 1000))

    def scrape_tweets_on_page(self, time_to_scroll):
        milli_start = self.current_time_millis()
        milli_current = self.current_time_millis()
        while milli_current - milli_start < time_to_scroll:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.sleep_range(1, 3)
            milli_current = self.current_time_millis()

        # Scrape Tweets
        self.tweets = self.browser.find_elements_by_class_name('TweetTextSize.js-tweet-text.tweet-text')
        regex = re.compile(r'[\n\r\t]');
        # Remove \n, \r, and \t from the tweets.
        for i in range(len(self.tweets)):
            self.formatted_tweets.append(regex.sub('', self.tweets[i].text))

        # Scrape Image Urls
        image_elements = self.browser.find_elements_by_class_name('AdaptiveMedia-photoContainer.js-adaptive-photo')
        for image in image_elements:
            self.image_urls.append(image.get_attribute('data-image-url'))

        print('Num Tweets: ' + str(len(self.tweets)))
        print('Num Images: ' + str(len(self.image_urls)))

    def download_remote_image(self, remote_url):
        request.urlretrieve(remote_url, 'tmpImage.jpg')
        print('downloaded image')
