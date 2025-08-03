# app/retrain_models.py

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os

# Load dataset
df = pd.read_csv("data/processed/movies.csv")

# Combine genres into a string
df['combined_genres'] = df[['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']].apply(
    lambda row: ' '.join([col for col in row.index if row[col] == 1]), axis=1
)

# Train TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_genres'])

# Train Nearest Neighbors
nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
nn_model.fit(tfidf_matrix)

# Save models
os.makedirs("models", exist_ok=True)
with open("models/tfidf.pkl", "wb") as f:
    pickle.dump(tfidf, f)

with open("models/nn_model.pkl", "wb") as f:
    pickle.dump(nn_model, f)

print("✅ Models saved in models/")
