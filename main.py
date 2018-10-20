import markovify


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


def main():
    print('Welcome to TrendyTwitter Bot!')
    print('Attempting sherlock holmes tweets..')

    mark = Markov('resources/rawText.txt')
    mark.build_tweet()


if __name__ == '__main__':
    main()
