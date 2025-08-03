# app/recommender.py

import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/processed/movies.csv")
df['combined_genres'] = df[['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']].idxmax(axis=1)

# === Load models ===
with open("models/tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("models/nn_model.pkl", "rb") as f:
    nn_model = pickle.load(f)

tfidf_matrix = tfidf.transform(df['combined_genres'])

def get_content_recommendations(movie_title, top_n=5):
    idx = df[df['title'] == movie_title].index
    if idx.empty:
        return pd.DataFrame()
    
    idx = idx[0]
    distances, indices = nn_model.kneighbors(tfidf_matrix[idx], n_neighbors=top_n + 1)
    indices = indices.flatten()[1:]

    recs = df.iloc[indices][['title']]
    recs['genres'] = df.iloc[indices]['combined_genres']
    return recs
