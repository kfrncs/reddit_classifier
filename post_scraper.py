#!/usr/bin/env python3
"""
Reddit Classifier: Post Scraper

To collect posts from two SubReddits and save a CSV of the corpus.
"""

# imports
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

    def __init__(self, subreddit='conspiracytheories'):
        ''' A class to scrape Reddit posts for bag-of-words NLP'''

        # "after" attribute for tracking how far we have scraped into the sub's history
        self.after = None
        # set subreddit to scrape
        self.subreddit = subreddit
        # empty attributes
        self.content = []
        

    def scrape(self, pages=5):
        """ fetch posts from Reddit API. Iterations chooses how many pages to scrape. """

        for i in range(1, pages+1):
            # if self.after exists, start from that post
            if self.after:
                self.last_request = requests.get(f'https://www.reddit.com/r/{self.subreddit}.json?after={self.after}',
                                            headers=headers)
                print(f'fetched page {i}')

            # else start at the beginning
            else:
                self.last_request = requests.get(f'https://www.reddit.com/r/{self.subreddit}.json',
                                            headers=headers)
                print(f'fetched page {i}')

            # parse JSON from the last request, inplace
            self.last_request = json.loads(self.last_request.text)

            # iterate through posts in most recently fetched JSON
            for post in range(len(self.last_request['data']['children'])):

                # If post has a "selftext" field, append it to the content list
                if self.last_request['data']['children'][post]['data']['selftext']:    
                    self.content.append(self.last_request['data']['children'][post]['data']['selftext'])
                    print(f'appended selftext from post {post}')

                # If post has "title", append it to content list
                elif self.last_request['data']['children'][post]['data']['title']:
                    self.content.append(self.last_request['data']['children'][post]['data']['title'])
                    print(f'appended title from post {post}')


    #   if 'selftext':
    #   last_request['data']['children'][0]['data']['selftext'])
    #   just title:
    #   last_request['data']['children'][i]['data']['title']

        # make post_after read where to start for next request
        self.after = self.last_request['data']['after']

        return self

    def combine_to_df():
        """ Combine scraped lists into a single df """
        return self 

if __name__ == "__main__":
    """ Scrape two subreddits, combine, save to csv. """

    # scrape(subreddit_a)
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_TOKEN)
    print('client_auth ran')

    ct = Scraper()
    ct.scrape()

