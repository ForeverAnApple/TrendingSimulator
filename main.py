from urllib.parse import quote
from cloudvision import VisionApi

from tweetcache import TweetCache
from bot import Bot
from markov import Markov

def main():
    cache = TweetCache()
    # vision = VisionApi()

    bot = Bot()
    user, passw = open('twitter_login.key', 'r').readline().split(' ')
    bot.login(user, passw)

    bot.select_trending_topics()

    # Get list of current trends and ask the user which one they want to use
    print("Current trends on twitter:")
    for i, name in enumerate(bot.trending_elements_names):
        print("  %d. %s" % (i + 1, name.text))

    print('Would you like to choose a trending tag (0), or enter your own tag/username (1)?: ')
    user_option = int(input())
    if user_option == 0:
        # click trending from the side bar
        selected_trend_index = int(input("Select a trend [1 thru %d]: " % (len(bot.trending_elements_names)))) - 1
        selected_trend = bot.trending_elements_names[selected_trend_index]
        selected_trend_text = selected_trend.text
    else:
        # the user is going to enter their own tag/user to scrape.
        selected_trend_text = input('Enter the tag you want to search for: ')
        if selected_trend_text.startswith('@'):
            bot.navigate('https://twitter.com/' + selected_trend_text[1:])
        elif selected_trend_text.startswith('#'):
            bot.navigate('https://twitter.com/search?q=%23' + selected_trend_text[1:] + '&src=tyah')
        else:
            bot.navigate('https://twitter.com/search?f=tweets&q=' + quote(selected_trend_text) + '&src=typd')

    # Load in new tweets if the cache misses
    if cache.cache_age(selected_trend_text) > 30*60:  # 30 minutes
        if user_option == 0:
            bot.trending_dictionary[selected_trend].click()

        bot.sleep_range(3, 7)
        bot.scrape_tweets_on_page(60*1000)

        cache.add_tweets(bot.formatted_tweets, selected_trend_text)
        cache.add_images(bot.image_urls, selected_trend_text)
        notag_images = cache.get_notag_images(selected_trend_text)

    # Grab tweets from cache and prep for markov ingestion
    all_text = ''
    tweet_count = 0
    for tweet in cache.get_tweets(selected_trend_text):
        tweet_count += 1
        if not tweet.endswith('.'):
            all_text = all_text + tweet + '. '
        else:
            all_text = all_text + tweet + ' '
    print("Loaded %d tweets" % tweet_count)

    # Generate new tweets
    while True:
        tweet_generator = Markov(all_text)
        suggested_tweets = [tweet_generator.build_tweet(selected_trend_text) for _ in range(5)]
        print("Suggested tweets:")
        for i, tweet in enumerate(suggested_tweets):
            print("  %d. %s" % (i + 1, tweet))

        choice = int(input("Select a tweet to publish [1 thru %d] or 0 to regenerate: " % len(suggested_tweets)))
        if choice > 0:
            bot.send_tweet(suggested_tweets[choice - 1])
            break


if __name__ == '__main__':
    main()
