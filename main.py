import markovify
from selenium import webdriver
from random import randint
import time
from tweetcache import TweetCache

class Markov:
    def build_tweet(self):
        print('Building tweet....')
        text_model = markovify.Text(self.text)

        tweet = text_model.make_short_sentence(140)
        while len(tweet) < 70:
            tweet = text_model.make_short_sentence(140)
        print(tweet)

    def __init__(self, resource_location):
        print('trying to open file')
        with open(resource_location) as f:
            raw_text = f.read()
        self.text = raw_text
        print('finished initializing')


class Bot:
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.trending_dictionary = {}
        self.trending_elements_names = []
        self.tweets = []
        self.image_urls = []

    def navigate(self, url):
        self.browser.get(url)

    @staticmethod
    def sleep_range(min, max):
        time.sleep(randint(min, max))

    @staticmethod
    def click_on_element(element_to_click):
        element_to_click.click()

    def login(self, username, password):
        # Navigate to the login page
        self.navigate('https://twitter.com/login')
        # Sleep for random amount of time
        self.sleep_range(1, 3)
        # Click the username field
        username_field = self.browser.find_element_by_class_name('js-username-field')
        username_field.send_keys(username)
        self.sleep_range(1, 3)
        # Click the password field
        password_field = self.browser.find_element_by_class_name('js-password-field')
        password_field.send_keys(password)
        self.sleep_range(1, 3)
        # Click the Log in button
        login_button = self.browser.find_element_by_class_name('submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
        login_button.click()
        print('Done')

    def send_tweet(self, tweet_to_send):
        # Navigate to twitter home page
        self.navigate('https://twitter.com/')
        # Type into the tweet field
        tweet_field = self.browser.find_element_by_id('tweet-box-home-timeline')
        tweet_field.send_keys(tweet_to_send)
        self.sleep_range(3, 5)
        # Click the tweet button
        tweet_button = self.browser.find_element_by_class_name('tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
        tweet_button.click()

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

        # For now go ahead and click on the first option
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
        tweets = self.browser.find_elements_by_class_name('TweetTextSize.js-tweet-text.tweet-text')
        # Scrape Image Urls
        image_elements = self.browser.find_elements_by_class_name('AdaptiveMedia-photoContainer.js-adaptive-photo')
        for image in image_elements:
            self.image_urls.append(image.get_attribute('data-image-url'))

        print('Num Tweets: ' + str(len(tweets)))
        print('Num Images: ' + str(len(self.image_urls)))


def main():
    cache = TweetCache()

    bot = Bot()
    bot.login('TrendySimulator', '7mDZJ7PEfbdie77')
    bot.sleep_range(1, 3)
    bot.select_trending_topics()

    print("Current trends on twitter:")
    for i, name in enumerate(bot.trending_elements_names):
        print("  %d. %s " % (i + 1, name.text))

    selected_trend_index = int(input("Select a trend [1 thru %d]: " % (len(bot.trending_elements_names)))) - 1
    selected_trend = bot.trending_elements_names[selected_trend_index]
    selected_trend_text = selected_trend.text

    bot.trending_dictionary[selected_trend].click()
    bot.sleep_range(3, 7)

    bot.scrape_tweets_on_page(30000)

    cache.add_tweets(bot.tweets, selected_trend_text)

    for tweet in bot.tweets:
        print(tweet.text)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    #text_model = markovify.Text(string)


if __name__ == '__main__':
    main()
