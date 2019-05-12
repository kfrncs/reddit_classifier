#!/usr/bin/env python3
"""
Data Cleaning
"""

# imports
import pandas as pd

def df_to_list(df):
    """ Take a DataFrame, return a list with all the values from 'document' """
    df_list = list(df['document'].values)
    return df_list

def drop_punctuation(in_list):
    """ drop all the punctuation from a list of strings"""
    out_list = in_list.copy()

    for i in range(len(out_list)):
        out_list[i] = out_list[i].replace('.', '').replace(',', '').replace('\'', '').replace('"', '')
        out_list[i] = out_list[i].replace('/', '').replace('\\', '').replace('!', '').replace('‘', '')
        out_list[i] = out_list[i].replace('“', '').replace('(', '').replace(')', '').replace('”', '')
        out_list[i] = out_list[i].replace('?', '')
        out_list[i] = out_list[i].replace(':', '').replace('’', '').lower()

    return out_list

td_df = pd.read_csv('data/td-2019-05-11.csv')
ct_df = pd.read_csv('data/ct-2019-05-11.csv')

td_list = df_to_list(td_df)
ct_list = df_to_list(ct_df)

td_list = drop_punctuation(td_list)
ct_list = drop_punctuation(ct_list)

td_list = td_list[:12000]
ct_list = td_list[:12000]



