from post_scraper import Scraper, headers
from spacy_model_creation import string_tokenizer, list_tokenizer, df_to_list
import numpy as np
from joblib import dump, load

vectorizer = load('vectorizer.joblib')
knn = load('knn.joblib')

td = Scraper('the_donald', category=0)
td.scrape(1)
td.content = list_tokenizer(td.content)
td.content_to_csv()

ct = Scraper('conspiracytheories', category=1)
ct.scrape(1)
ct.content = list_tokenizer(ct.content)
ct.content_to_csv()

td.vectorized = vectorizer.transform(td.content)
ct.vectorized = vectorizer.transform(ct.content)

td.preds = knn.predict(td.vectorized)
ct.preds = knn.predict(ct.vectorized)

print("posts from the_donald (0): ", td.preds)
print("predictions from ConspiracyTheories (1):", ct.preds)

