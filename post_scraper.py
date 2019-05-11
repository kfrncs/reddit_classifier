#!/usr/bin/env python3
"""
Reddit Classifier: Post Scraper

To collect posts from two SubReddits and save a CSV of the corpus.
"""
import requests
import os
import json

# load environment variables from .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# load Reddit Token/Client_ID from .env
REDDIT_TOKEN = os.environ['REDDIT_TOKEN']   
REDDIT_ID = os.environ['REDDIT_ID']   

# set headers for API requests
headers = {"Authorization": REDDIT_ID + REDDIT_TOKEN, "User-Agent": "reddit_scraping/0.1 by kfrncs"}


class Scraper:

    def __init__(self, subreddit_a='conspiracytheories', subreddit_b='the_donald'):
        ''' A class to scrape Reddit posts for bag-of-words NLP'''
        # "after" attribute for tracking how far we have scraped into the sub's history
        self.after = None
        
        # set subreddits to scrape
        self.subreddit_a = subreddit_a
        self.subreddit_b = subreddit_b
        
        
    def scrape(self, subreddit):
        """ fetch posts from Reddit API"""

        if self.after:
            self.last_request = requests.get(f'https://www.reddit.com/r/{subreddit}.json?after={after}',
                                        headers=headers)
        else:
            self.last_request = requests.get(f'https://www.reddit.com/r/{subreddit}.json',
                                        headers=headers)

        # parse JSON from the last request, inplace
        self.last_request = json.loads(self.last_request.text)
    #   if 'selftext':
    #   last_request['data']['children'][0]['data']['selftext'])
    #   just title:
    #   last_request['data']['children'][i]['data']['title']

        # make post_after read where to start for next request
        self.post_after = self.last_request['data']['after']

        return self

    def combine_to_df():
        """ Combine scraped lists into a single df """
        return self 

if __name__ == "__main__":
    """ Scrape two subreddits, combine, save to csv. """
    # scrape(subreddit_a)
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_TOKEN)
    print('client_auth ran')
    
    scraper = Scraper()
    scraper.scrape(scraper.subreddit_a)
    # test['data']['children'][0]['data']['selftext']
    # oh jeez

