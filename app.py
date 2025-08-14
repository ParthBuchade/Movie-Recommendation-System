import streamlit as st
import pickle
import requests
import time

# Placeholder image for missing posters
DEFAULT_POSTER = "https://via.placeholder.com/500x750?text=No+Image"

# Function to fetch poster from TMDB API with retries and fallback
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f918f07200934165a338dc1390605b57&language=en-US'
    for attempt in range(3):  # Try up to 3 times
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('poster_path'):
                return "https://image.tmdb.org/t/p/original/" + data['poster_path']
            else:
                return DEFAULT_POSTER
        except Exception as e:
            if attempt < 2:
                time.sleep(1)  # Wait before retry
            else:
                st.warning(f"Poster fetch failed for ID {movie_id}: {e}")
                return DEFAULT_POSTER

# Function to recommend movies
def recommend(movie):
    movie_index = mlist[mlist['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    movies_poster = []
    
    for i in movie_list:
        movie_id = mlist.iloc[i[0]].movie_id  # actual TMDB movie ID
        recommend_movies.append(mlist.iloc[i[0]].title)
        time.sleep(0.2)  # small delay to avoid hitting rate limits
        movies_poster.append(fetch_poster(movie_id))
    
    return recommend_movies, movies_poster

# Load data
movies_list = pickle.load(open('movies.pkl', 'rb'))
mlist = movies_list  # keep full DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Select a movie to get recommendations',
    mlist['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)   
    cols = st.columns(5)  # display 5 recommendations side by side
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx])
            st.caption(names[idx])
