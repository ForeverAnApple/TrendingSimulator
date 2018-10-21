# TrendingSimulator
This is a Twitter bot that uses a Markov chain in order to become the most "trendy human" on Twitter.
It is created in the same vein as the "/r/SubredditSimulator" bots. 

This was created during a 36 hour time period at the Hack K-State hackathon.  

### How it works

Through clever web-scraping, TrendingSimulator will fetch the "Top Trending" from any 
defined region. It will take these trends, analyze and parse the related tweets using [markovify](https://github.com/jsvine/markovify)
(the same as Subreddit Simulator), and create 140 character tweets with that information. 

## Installation

### Pre-requisites:
1. ```clone https://github.com/ForeverAnApple/TrendingSimulator/```

1. Python 3.7

1. [markovify](https://github.com/jsvine/markovify)

1. Selenium
    1. [Geckodriver](https://github.com/mozilla/geckodriver/) (Firefox)
    1. [Chromedriver](http://chromedriver.chromium.org/downloads) (Chrome/Chromium)

1. Google Cloud Vision API
    1. Google Cloud Vision [Authentication](https://cloud.google.com/vision/docs/auth)
    2. Create `cloud-vision.key` in your root directory with the Google Cloud Vision API Key


### Set-up
1. Create `twitter_login.key` in your root directory with your twitter bot username and password (space separated).

2. Check the requirements.txt file.

3. Install all dependencies. 

4. Make sure your Selenium drivers are inside your PATH.
    1. You can also run Chromedriver without adding it to your path before running `main.py`

5. Run main.py
    1. `python3 main.py`

### Additional Information
#### Scraping
* Selenium creates a wrapper around the web browser. Normally used for unit testing, we are using it to scrape twitter.
##### Headless Mode
* By default, your browser should open and give a good demo on how the scraping and posting works. However, if the user wants to, it is possible to run purely in a commandline interface.

#### Caching
* Looks like Selenium takes a while to scrape pages, to make this process more efficient. We will cache tweets 
and renew them every 30 minutes.

* Google Cloud Vision API is not cheap! To save requests, caching is used on image tags. Cached data on a certain subject line lasts 
30 minutes by default before scraping again.

* Also to save money, the API will send the least amount of requests neccesary to sending the maximum number of 
pictures (16) in every request.

* A(n) [sqlite](https://www.sqlite.org) database is used to store tweets, image information, and image tags information.

#### Image Labeling and Selection
* Images will be labeled and tagged with Google Cloud Vision and loaded into the database.

* During image selection phase, images will be matched to the tweet using the tags given to the images. The program will
choose the most "relevant" image by seeing how well the tags match with the tweet itself.





### Created by:
* [Alex Gittemeier](https://github.com/win93)
* [Daiwei Chen](https://github.com/ForeverAnApple)
* [Joseph Watts](https://github.com/JosephCW)
* [Michael Burnes](https://github.com/mburnes)
