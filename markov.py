import markovify


class Markov:
    def build_tweet(self, phrase):
        tweet = self.make_tweet_with_tag(phrase)
        while len(tweet) < 70:
            tweet = self.make_tweet_with_tag(phrase)
        return tweet

    def make_tweet_with_tag(self, phrase):
        return Markov.add_tag(self.text_model.make_short_sentence(140), phrase)

    @staticmethod
    def add_tag(current, tag):
        if tag not in current:
            if tag.startswith('#'):
                return '#' + current + ' ' + tag
            elif not tag.startswith('@'):
                return tag + ': ' + current
        return current

    def __init__(self, raw_text):
        self.text_model = markovify.Text(raw_text)
