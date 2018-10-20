import markovify

class Markov:
    def build_tweet(self):
        # print('Building tweet....')
        text_model = markovify.Text(self.text)

        tweet = text_model.make_short_sentence(140)
        while len(tweet) < 70:
            tweet = text_model.make_short_sentence(140)
        return tweet

    def __init__(self, raw_text):
        print('trying to initialize text with all tweets.')
        self.text = raw_text
