#!/usr/bin/env python3
"""
Reddit Classifier: Post Scraper

To collect posts from two SubReddits and save a CSV of the corpus.
"""

# imports
import requests
import os
import json
import pandas as pd
from time import sleep

# load environment variables from .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# load Reddit Token/Client_ID from .env
REDDIT_TOKEN = os.environ['REDDIT_TOKEN']   
REDDIT_ID = os.environ['REDDIT_ID']   

# set headers for API requests
headers = {"Authorization": REDDIT_ID + REDDIT_TOKEN, "User-Agent": "reddit_scraping/0.1 by kfrncs"} 


class Scraper:

    def __init__(self, subreddit, category='unknown'):
        ''' A class to scrape Reddit posts for bag-of-words NLP'''

        # "after" attribute for tracking how far we have scraped into the sub's history
        # see for more: https://www.reddit.com/dev/api/
        self.after = None
        # set subreddit to scrape
        self.subreddit = subreddit
        # empty content list to append titles/post content
        self.content = []

        # category must be set for the corpus
        if category == 'unknown':
            self.category = input(f'Please input the category for {self}')
        else:
            self.category = category


    def scrape(self, pages=3):
        """ fetch posts from Reddit API. Iterations chooses how many pages to scrape. """

        for page in range(1, pages+1):
            # if self.after exists, start from that post
            if self.after:
                self.last_request = requests.get(f'https://www.reddit.com/r/{self.subreddit}.json?after={self.after}',
                                            headers=headers)
                print(f'fetched page {page}')

            # else start at the beginning
            else:
                self.last_request = requests.get(f'https://www.reddit.com/r/{self.subreddit}.json',
                                            headers=headers)
                print(f'fetched page {page}')

            # parse JSON from the last request, inplace
            self.last_request = json.loads(self.last_request.text)
            print(f'Parsed page {page} as JSON')

            # iterate through posts in most recently fetched JSON
            for post in range(len(self.last_request['data']['children'])):
                
                # If post has "title", append it to content list
                if self.last_request['data']['children'][post]['data']['title']:
                    self.content.append(self.last_request['data']['children'][post]['data']['title'])
                    print(f'appended post {post}, page {page} to {self.category}.content.')

            # avoid Error 429
            sleep(1.6)
            print('slept 1.6 seconds')

            # make post_after read where to start for next request
            self.after = self.last_request['data']['after']
            print('updated "after"')

            self.content_to_csv()
            print('saved csv')

        return self


    def content_to_csv(self):
        """ Stores content to df, outputs a DataFrame with the date and name of SubReddit """
        self.df = pd.DataFrame(self.content, columns=['document'])
        self.df['category'] = self.category

        self.df.to_csv(f'data/{self.category}-{pd.datetime.now().strftime("%Y-%m-%d")}.csv', index=False)

        return self



if __name__ == "__main__":
    """ Scrape two subreddits, combine, save to csv. """

    client_auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_TOKEN)
    print('client_auth ran')

    td = Scraper('the_donald', category=0)
    td.scrape()

    ct = Scraper('conspiracytheories', category=1)
    ct.scrape()


