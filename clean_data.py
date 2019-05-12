#!/usr/bin/env python3
"""
Data Cleaning
"""

# imports
import pandas as pd
from nltk.tokenize import RegexpTokenizer

def df_to_str(df):
    """ Take a DataFrame, return a string with all the values in 'document' joined together """
    df_list = list(df['document'].values)
    df_str = ' '.join(df_list)
    return df_str

td_df = pd.read_csv('data/td-2019-05-11.csv')
ct_df = pd.read_csv('data/ct-2019-05-11.csv')

td_str = df_to_str(td_df)
ct_str = df_to_str(ct_df)

tokenizer = RegexpTokenizer(r'\w+')


