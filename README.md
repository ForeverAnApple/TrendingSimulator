# TrendingSimulator
This is a Twitter bot that uses a Markov chain in order to become the most "trendy human" on Twitter.
It is created in the same vein as the "/r/SubredditSimulator" bots. 

This was created during a 36 hour time period at the Hack K-State hackathon.  

### How it works

Through clever web-scraping, TrendingSimulator will fetch the "Top Trending" from any 
defined region. It will take these trends, analyze and parse the related tweets using [markovify](https://github.com/jsvine/markovify)
(the same as Subreddit Simulator), and create 140 character tweets with that information. 

## Installation

### Requisites:
1. ```clone https://github.com/ForeverAnApple/TrendingSimulator/```
1. Python 3.7
1. [markovify](https://github.com/jsvine/markovify)
1. Selenium
    1. [Geckodriver](https://github.com/mozilla/geckodriver/) (Firefox)
    1. [Chromedriver](http://chromedriver.chromium.org/downloads) (Chrome/Chromium)
1. Google Cloud Vision API
    1. Google Cloud Vision [Authentication](https://cloud.google.com/vision/docs/auth)
    2. Create `cloud-vision.key` in your root directory with the Google Cloud Vision API Key
1. Create `twitter_login.key` in your root directory with your twitter bot username and password (space separated).
2. Check the requirements.txt file.
3. Install all dependencies. 
4. Make sure your Selenium drivers are inside your PATH.
    1. You can also run Chromedriver without adding it to your path before running `main.py`
5. Run main.py
    1. `python3 main.py`


#### Created by:
* [Alex Gittemeier](https://github.com/win93)
* [Daiwei Chen](https://github.com/ForeverAnApple)
* [Joseph Watts](https://github.com/JosephCW)
* [Michael Burnes](https://github.com/mburnes)
