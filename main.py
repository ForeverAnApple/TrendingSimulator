from urllib.parse import quote
import re
import random

from tweetcache import TweetCache
from bot import Bot
from markov import Markov


def suggest_image(cache, tweet, topic):
    urls = []
    for match in re.finditer('[a-zA-Z]+', tweet):
        # print(match.group(0), end=' ')
        for url in cache.get_images_for_word(match.group(0)):
            urls.append(url)
            # print('x', end='')
        # print('')
    if len(urls) == 0:
        print("Did not find any text-to-tag matches. Falling back to topic-to-topic matches.")
        for url in cache.get_images_for_topic(topic):
            urls.append(url)
    return random.choice(urls) if len(urls) > 0 else None


def main():
    cache = TweetCache()

    bot = Bot()
    user, passw = open('twitter_login.key', 'r').readline().split(' ')
    bot.login(user, passw)

    bot.select_trending_topics()

    # Get list of current trends and ask the user which one they want to use
    print("Current trends on twitter:")
    for i, name in enumerate(bot.trending_elements_names):
        print("  %d. %s" % (i + 1, name.text))

    user_option = int(input('Select a trend [1 thru %d], or type 0 for a custom search: ' % len(bot.trending_elements_names)))
    if user_option != 0:
        # click trending from the side bar
        selected_trend = bot.trending_elements_names[user_option - 1]
        selected_trend_text = selected_trend.text
    else:
        # the user is going to enter their own tag/user to scrape.
        selected_trend_text = input('Enter the tag you want to search for: ')

    # Load in new tweets if the cache misses
    if cache.cache_age(selected_trend_text) > 30 * 60:  # 30 minutes
        if user_option != 0:
            bot.trending_dictionary[selected_trend].click()
        else:
            if selected_trend_text.startswith('@'):
                bot.navigate('https://twitter.com/' + selected_trend_text[1:])
            elif selected_trend_text.startswith('#'):
                bot.navigate('https://twitter.com/hashtag/' + selected_trend_text[1:])
            else:
                bot.navigate('https://twitter.com/search?f=tweets&q=' + quote(selected_trend_text) + '&src=typd')

        # If it isn't a users page click to get the newest posted items.
        print("Setting up webpage to begin scraping...")
        if not selected_trend_text.startswith('@'):
            bot.browser.implicitly_wait(5)
            latest_button = bot.browser.find_elements_by_class_name(
                'AdaptiveFiltersBar-target.AdaptiveFiltersBar-target--link.js-nav.u-textUserColorHover')
            # first one is top, 2nd is latest, 3rd people, 4th videos
            bot.sleep_range(1, 3)
            latest_button[1].click()
            bot.sleep_range(5, 10)
            bot.browser.implicitly_wait(5)

        bot.sleep_range(3, 7)
        bot.scrape_tweets_on_page(60 * 1000)

        cache.add_tweets(bot.formatted_tweets, selected_trend_text)
        cache.add_images(bot.image_urls, selected_trend_text)

        # Google cloud services
        print("Contacting google(tm) Cloud(r) services(sm)...")
        notag_images = cache.get_notag_images(selected_trend_text)
        cache.add_image_tags(notag_images, selected_trend_text)
    else:
        print("Cache hit!")

    # Grab tweets from cache and prep for markov ingestion
    all_text = ''
    tweet_count = 0
    for tweet in cache.get_tweets(selected_trend_text):
        tweet_count += 1
        if not tweet.endswith('.'):
            all_text = all_text + tweet + '. '
        else:
            all_text = all_text + tweet + ' '
    print("Loaded %d tweets from cache" % tweet_count)

    # Generate new tweets
    while True:
        tweet_generator = Markov(all_text)
        suggested_tweets = []
        print("Suggested tweets:")
        for i in range(5):
            tweet = tweet_generator.build_tweet(selected_trend_text)
            image = suggest_image(cache, tweet, selected_trend_text)
            print("  %d. %s (%s)" % (i + 1, tweet, image))
            suggested_tweets.append((tweet, image))

        choice = int(input("Select a tweet to publish [1 thru %d] or 0 to regenerate: " % len(suggested_tweets)))
        if choice > 0:
            tweet, image = suggested_tweets[choice - 1]
            if image is not None:
                bot.download_remote_image(image)
            bot.send_tweet(tweet, image is not None)
            break


if __name__ == '__main__':
    main()
