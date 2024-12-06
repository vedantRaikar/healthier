from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_keywords(text, top_n=40):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[::-1]
    top_keywords = [feature_array[i] for i in tfidf_sorting[:top_n]]
    return top_keywords



