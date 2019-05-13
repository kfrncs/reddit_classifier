#!/usr/bin/env python3
"""

Spacy Model Creation

"""

# imports
from joblib import dump, load
import string
import pandas as pd
import spacy
from spacy.lang.en import English

# sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import ComplementNB

# load spacy model, set the stopwords
print('loading spacy en_core_web_sm')
nlp = spacy.load('en_core_web_sm')

print('loading spacy stopwords')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

# set the parser, bring in punctuation
parser = English()
punctuation = string.punctuation

def string_tokenizer(post):
    """ Parse posts and tokenize 
    
        adapted from https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/
    """

    my_tokens = parser(post)
    # -PRON- bit is for pronouns: https://spacy.io/api/annotation#lemmatization
    my_tokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in my_tokens ]
    my_tokens = [ word for word in my_tokens if word not in spacy_stopwords and word not in punctuation ]

    return ' '.join(my_tokens)


# HEY MAX - is there a cleaner way to do this??
def list_tokenizer(input_list):
    """ string_tokenizes through lists """

    output_list = []

    for post in range(0, len(input_list)):
        output_list.append(string_tokenizer(input_list[post]))
        print(f'tokenized {post} in list_tokenizer')

    return output_list


def df_to_list(df):
    """ Take input DataFrame, return a list with all the values from 'document' """
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

    td_list = td_list[:12000]
    print('shortened td_list')
    ct_list = ct_list[:12000]
    print('shortened ct_list')

    print('starting Spacy tokenization on td_list')
    td_list = list_tokenizer(td_list)

    print('starting Spacy tokenization on ct_list')
    ct_list = list_tokenizer(ct_list)

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

    # Vectorize
    vectorizer = CountVectorizer(max_features=5000)     
    train_data_features = vectorizer.fit_transform(x_train)
    test_data_features = vectorizer.transform(x_test)
    vocab = vectorizer.get_feature_names()
    print('trained and transformed w/ vectorizer')
    dump(vectorizer, 'vectorizer.joblib')

    # model training
    log_reg = LogisticRegression()
    log_reg.fit(train_data_features, y_train)
    lr_preds = log_reg.predict(test_data_features) 

    # keep the knn, it's the best
    knn = KNeighborsClassifier()
    knn.fit(train_data_features, y_train)
    knn_preds = knn.predict(test_data_features) 
    dump(knn, 'knn.joblib')

    cnb = ComplementNB()
    cnb.fit(train_data_features, y_train)
    cnb_preds = cnb.predict(test_data_features) 

    # make df with all preds
    df = pd.DataFrame(list(zip(cnb_preds, lr_preds, knn_preds, y_test, x_test)), 
                      columns=['cnb_preds', 'lr_preds', 'knn_preds', 'category', 'document'])

    # save incorrect predictions in a df to look at 
    lr_incorrect = df[df['lr_preds'] != df['category']].copy()
    knn_incorrect = df[df['knn_preds'] != df['category']].copy()
    cnb_incorrect = df[df['cnb_preds'] != df['category']].copy()

    # combine lr and knn incorrects
    two_incorrect = knn_incorrect[knn_incorrect['lr_preds'] != knn_incorrect['category']].copy()
    all_incorrect = two_incorrect[two_incorrect['cnb_preds'] != two_incorrect['category']].copy()

    print('knn score: ', knn.score(test_data_features, y_test))
    print('log_reg score: ', log_reg.score(test_data_features, y_test))
    print('ComplementNaiveBayes score: ', cnb.score(test_data_features, y_test))

