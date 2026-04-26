import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API")

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        /* Plain white background */
        [data-testid="stAppViewContainer"] {
            background: #ffffff !important;
            position: relative;
            overflow: hidden;
        }
        
        /* Main container */
        .main {
            background: transparent !important;
            position: relative;
            z-index: 1;
        }
        
        /* Main title styling */
        .main-title {
            text-align: center;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FF6B6B, #FFE66D, #4ECDC4, #FF6B6B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            animation: fadeIn 1s ease-in;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
            font-weight: 600;
        }
        
        /* Movie card styling - Classy and minimal */
        .movie-card {
            background: transparent;
            border-radius: 20px;
            padding: 1rem 0;
            transition: all 0.3s ease;
            height: 100%;
            cursor: pointer;
            position: relative;
        }
        
        .movie-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1;
            pointer-events: none;
        }
        
        .movie-card:hover::before {
            opacity: 1;
            border-color: rgba(255, 215, 0, 0.4);
        }
        
        .movie-card:hover {
            transform: translateY(-15px) !important;
        }
        
        .movie-title {
            color: #1a1a1a;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1rem;
            font-size: 1rem;
            line-height: 1.5;
            text-shadow: 0 1px 3px rgba(255, 255, 255, 0.5);
            word-wrap: break-word;
            position: relative;
            z-index: 2;
            letter-spacing: 0.5px;
            transition: transform 0.3s ease !important;
            display: inline-block;
            width: 100%;
        }
        
        .movie-card:hover .movie-title {
            transform: scale(1.15) !important;
            letter-spacing: 1px;
        }
        
        .movie-link {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.7rem 1.5rem;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 800;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
            cursor: pointer;
            z-index: 3;
            position: relative;
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }
        
        .movie-link:hover {
            transform: scale(1.1) translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5);
            text-decoration: none;
        }
        
        .movie-link:active {
            transform: scale(0.95);
        }
        
        /* Image styling */
        .movie-image {
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 2;
            width: 100%;
            display: block;
            transition: transform 0.3s ease !important, filter 0.3s ease !important;
        }
        
        /* Hover effect for images - STRONG ENLARGE */
        .movie-card:hover .movie-image {
            filter: brightness(1.2) drop-shadow(0 0 20px rgba(255, 215, 0, 0.4)) !important;
            transform: scale(1.25) !important;
        }
        
        /* Heading styling */
        h1, h2, h3, h4, h5, h6 {
            color: #333 !important;
            font-weight: 800 !important;
        }
        
        /* Select box and input styling */
        .stSelectbox, .stTextInput, .stNumberInput {
            background: rgba(255, 255, 255, 0.95) !important;
        }
        
        [data-testid="stSelectboxListbox"], .stSelectbox div {
            background: rgba(255, 255, 255, 0.98) !important;
        }
        
        /* Button styling */
        button[kind="primary"] {
            background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%) !important;
            color: #fff !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 30px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Divider styling */
        hr {
            border-color: rgba(0, 0, 0, 0.1) !important;
            margin: 2rem 0 !important;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Title with emoji
st.markdown(
    '<div class="main-title">🎬 Movie Recommender</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Discover your next favorite movie</div>',
    unsafe_allow_html=True
)

#Function for recommending movies

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ids = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_ids.append(movie_id)
    return recommended_movies, recommended_movies_posters, recommended_movies_ids

def fetch_poster(movie_id):
    try:
        if not TMDB_API_KEY:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        )
        data = response.json()
        if response.status_code == 200 and 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            # Return a placeholder image if poster_path is not available
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Loading movies_df and similarity matrix
movies_list = pickle.load(open("movies.pkl","rb"))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity_index.pkl','rb'))

if not TMDB_API_KEY:
    st.warning(
        "TMDB_API is not configured. Poster images will use a placeholder image. "
        "Set TMDB_API as a secret or environment variable in your deployment."
    )

# User movie selection with better styling
st.markdown("### 🎥 Select a Movie")
selected_movie = st.selectbox(
    "Choose a movie you like:",
    movies['title'].values,
    label_visibility="collapsed"
)

# Submit button with custom styling
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    recommend_btn = st.button("✨ Get Recommendations", use_container_width=True)

if recommend_btn:
    # Fetching images of movie
    with st.spinner("🎬 Finding perfect recommendations for you..."):
        names, posters, movie_ids = recommend(selected_movie)
    
    st.markdown("---")
    st.markdown("### 🌟 Top 5 Recommendations")
    st.markdown("")
    
    cols = st.columns(5, gap="medium")
    
    for idx, (col, name, poster, movie_id) in enumerate(zip(cols, names, posters, movie_ids)):
        with col:
            st.markdown(f'''
            <div class="movie-card">
                <div class="movie-title">{name}</div>
                <div style="display: flex; justify-content: center; overflow: hidden; border-radius: 15px;">
                    <img src="{poster}" class="movie-image" alt="{name}" style="width: 100%; height: auto; display: block;">
                </div>
                <div style="text-align: center;">
                    <a href="https://www.themoviedb.org/movie/{movie_id}" target="_blank" class="movie-link">🔗 View on TMDB</a>
                </div>
            </div>
            ''', unsafe_allow_html=True)
