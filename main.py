import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

data = pd.read_csv('ana-101.csv')


docs = data['title']
# print(docs)

vectorizer = TfidfVectorizer()
tfidf_docs = vectorizer.fit_transform(docs)


# query
query = 'دانشگاه تهران'
tfidf_query = vectorizer.transform([query])[0]

# similarities
cosines = []
for d in tfidf_docs:
  cosines.append(
    float(cosine_similarity(d, tfidf_query)))

# sorting
k = 10
sorted_ids = np.argsort(cosines)
for i in range(k):
  cur_id = sorted_ids[-i-1]
  print(docs[cur_id], cosines[cur_id])