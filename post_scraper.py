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

# set subreddits to scrape
subreddit_a = 'conspiracytheories'
subreddit_b = 'the_donald'

def scrape(subreddit):
    """ fetch posts from Reddit API"""
    last_request = requests.get(f'https://www.reddit.com/r/{subreddit}.json',
                                headers=headers)
    last_request = json.loads(last_request.text)
#   if 'selftext':
#   last_request['data']['children'][0]['data']['selftext'])
#   just title:
#   last_request['data']['children'][i]['data']['title']
    return last_request

def combine_to_df():
    """ Combine scraped lists into a single df """
    return df

if __name__ == "__main__":
    """ Scrape two subreddits, combine, save to csv. """
    # scrape(subreddit_a)
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_TOKEN)
    print('client_auth ran')

    # test['data']['children'][0]['data']['selftext']
    # oh jeez

