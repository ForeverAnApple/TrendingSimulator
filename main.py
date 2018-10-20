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


def main():
    bot = Bot()
    bot.login('TrendySimulator', '7mDZJ7PEfbdie77')
    bot.sleep_range(1, 3)



if __name__ == '__main__':
    main()
