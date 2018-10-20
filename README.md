# TrendingSimulator
This is a Twitter bot that uses a Markov chain in order to become the most "trendy human" on Twitter.
It is created in the same vein as the "/r/SubredditSimulator" bots. 

This was created during a 36 hour time period at the Hack K-State hackathon.  

### How it works

Through the [Tweepy API](https://github.com/tweepy/tweepy), TrendingSimulator will fetch the "Top Trending" from any 
defined region. It will take these trends, analyze and parse the tweets using [markovify](https://github.com/jsvine/markovify)
(the same as Subreddit Simulator), and create 140 character tweets with that information. 



### Requisites:
1. Python 3.7
1. [markovify](https://github.com/jsvine/markovify)
1. [Tweepy](https://github.com/tweepy/tweepy)


