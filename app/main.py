# app/main.py

import streamlit as st
import pandas as pd
from recommender import get_content_recommendations
from utils import fetch_poster_url

# ======================
# 🎨 UI Config
# ======================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

# ======================
# 🎯 Load Data
# ======================
movies = pd.read_csv("data/processed/movies.csv")
unique_titles = movies['title'].drop_duplicates().sort_values().tolist()

# ======================
# 🔍 Movie Selection
# ======================
selected_movie = st.selectbox("Select a movie to get recommendations", unique_titles)

if selected_movie:
    with st.spinner("🔄 Generating recommendations..."):
        recommendations = get_content_recommendations(selected_movie, top_n=5)

    if recommendations.empty:
        st.warning("⚠️ Sorry, no recommendations found for this movie.")
    else:
        st.markdown(f"### 🔎 Because you watched **{selected_movie}**, you may also like:")

        # Create dynamic columns
        num_recs = len(recommendations)
        cols = st.columns(num_recs)

        for idx, (_, row) in enumerate(recommendations.iterrows()):
            with cols[idx]:
                poster_url = fetch_poster_url(row['title'])
                st.image(poster_url, use_container_width=True)
                st.markdown(f"**{row['title']}**")
                st.caption(f"Genres: {row['genres']}")
