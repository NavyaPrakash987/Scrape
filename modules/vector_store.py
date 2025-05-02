from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

vectorizer = TfidfVectorizer(stop_words="english")
vector_matrix = None
corpus = []

def build_vector_store(docs):
    global vector_matrix, corpus
    corpus = list(docs.values())
    vector_matrix = vectorizer.fit_transform(corpus)
    return vector_matrix

def query_vector_store(query, top_n=5):
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, vector_matrix).flatten()
    top_indices = np.argsort(sims)[-top_n:][::-1]
    return [(corpus[i], sims[i]) for i in top_indices]
