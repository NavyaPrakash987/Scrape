from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from gensim.summarization import summarize
import nltk

nltk.download('punkt')

def extract_keywords(texts, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()
    scores = X.sum(axis=0).A1
    keywords_scores = sorted(zip(keywords, scores), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in keywords_scores[:top_n]]

def summarize_text(text):
    try:
        return summarize(text)
    except ValueError:
        return text
