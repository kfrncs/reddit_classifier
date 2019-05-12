#!/usr/bin/env python3
"""

Spacy Model Creation

"""

# imports
import string
import pandas as pd
import spacy
from spacy.lang.en import English
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split

# load spacy model, set the stopwords
print('loading spacy en_core_web_sm')
nlp = spacy.load('en_core_web_sm')

print('loading spacy stopwords')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

# set the parser, bring in punctuation
parser = English()
punctuation = string.punctuation

def spacy_tokenizer(post):
    """ Parse posts and tokenize 
    
        adapted from https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/
    """
    my_tokens = parser(post)
    
    # -PRON- bit is for pronouns: https://spacy.io/api/annotation#lemmatization
    my_tokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in my_tokens ]

    my_tokens = [ word for word in my_tokens if word not in spacy_stopwords and word not in punctuation ]
    
    return ' '.join(my_tokens)

def df_to_list(df):
    """ Take a DataFrame, return a list with all the values from 'document' """
    df_list = list(df['document'].values)
    return df_list


if __name__ == "__main__":
    
    td_df = pd.read_csv('data/td-2019-05-11.csv')
    print('loaded td_df')
    ct_df = pd.read_csv('data/ct-2019-05-11.csv')
    print('loaded ct_df')

    td_list = df_to_list(td_df)
    print('converted td_df to td_list')
    ct_list = df_to_list(ct_df)
    print('converted ct_df to ct_list')

    td_list = td_list[:1000]
    print('shortened td_list')
    ct_list = ct_list[:1000]
    print('shortened ct_list')
    
    print('starting Spacy tokenization on td_list')
    for post in range(len(td_list)):
        td_list[post] = spacy_tokenizer(td_list[post])
        print(f'tokenized {post} in td_list')

    print('starting Spacy tokenization on ct_list')
    for post in range(len(ct_list)):
        ct_list[post] = spacy_tokenizer(ct_list[post])
        print(f'tokenized {post} in ct_list')
 
    td_df = pd.DataFrame(td_list, columns=['document'])
    td_df['category'] = 0
    ct_df = pd.DataFrame(ct_list, columns=['document'])
    ct_df['category'] = 1
    print('created separate dataframes from lists')
    
    corpus = td_df.append(ct_df)
    print('combined dataframes')
    
    # Train_test_split
    x = corpus['document'].values
    y = corpus['category'].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    print('train_test_split')

    


    # do we need these?
    # tvec = TfidfVectorizer(stop_words='english')
    # tvec.fit(corpus)
    # corpus_matrix = tvec.transform(corpus)



