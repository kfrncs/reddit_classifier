#!/usr/bin/env python3
"""
Reddit Classifier: Post Scraper

To collect posts from two SubReddits and save a CSV of the corpus.
"""
import requests

subreddit_a = 'conspiracytheories'
subreddit_b = 'the_donald'

def scrape(subreddit):
    """ fetch posts from Reddit API"""
    scraped_list = requests.get(f'https://www.reddit.com/r/{subreddit}.json')
    return scraped_list

def combine_to_df():
    """ Combine scraped lists into a single df """
    return df

if __name__ == "__main__":
    """ This is executed when run from the command line """
    scrape(subreddit_a)
