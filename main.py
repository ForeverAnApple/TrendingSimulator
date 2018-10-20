import markovify
from selenium import webdriver
from random import randint
from time import sleep

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

    def navigate(self, url):
        self.browser.get(url)

    @staticmethod
    def sleep_range(min, max):
        sleep(randint(min, max))

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
        # Select trending hashtags parents
        trending_elements = self.browser.find_elements_by_class_name('pretty-link.js-nav.js-tooltip.u-linkComplex')
        trending_elements_names = self.browser.find_elements_by_class_name('u-linkComplex-target.trend-name')
        for x in range(len(trending_elements)):
            self.trending_dictionary[trending_elements_names[x]] = trending_elements[x]

        for x in trending_elements_names:
            print(x.text)

        self.trending_dictionary.get(trending_elements_names[0]).click()


def main():
    bot = Bot()
    bot.login('TrendySimulator', '7mDZJ7PEfbdie77')
    bot.sleep_range(1, 3)
    bot.select_trending_topics()

    text_model = markovify.Text(string)


if __name__ == '__main__':
    main()
