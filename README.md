# TrendingSimulator
This is a Twitter bot that uses a Markov chain in order to become the most "trendy human" on Twitter.
It is created in the same vein as the "/r/SubredditSimulator" bots. 

This was created during a 36 hour time period at the Hack K-State hackathon.  

### How it works

Through clever web-scraping, TrendingSimulator will fetch the "Top Trending" from any 
defined region. It will take these trends, analyze and parse the related tweets using [markovify](https://github.com/jsvine/markovify)
(the same as Subreddit Simulator), and create 140 character tweets with that information. 

### Planned features:


### Requisites:
1. Python 3.7
1. [markovify](https://github.com/jsvine/markovify)
1. Selenium
   1. [Geckodriver](https://github.com/mozilla/geckodriver/) (Firefox)
   1. [Chromedriver](http://chromedriver.chromium.org/downloads) (Chrome/Chromium)
1. Google Cloud Vision API
   1. Needs an API key.

## Installation




#### Created by:
* [win93](https://github.com/win93)
* [ForeverAnApple](https://github.com/ForeverAnApple)
* [JosephCW](https://github.com/JosephCW)
* [mburnes](https://github.com/mburnes)
