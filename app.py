import streamlit as st
import pickle
import requests

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f918f07200934165a338dc1390605b57&language=en-US'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"

    except Exception as e:
        st.warning(f"Poster fetch failed for ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    movie_index = mlist[mlist['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    
    recommend_movies = []
    movies_poster = []
    
    for i in movie_list:
        movie_id = mlist.iloc[i[0]].movie_id  # actual TMDB movie ID
        recommend_movies.append(mlist.iloc[i[0]].title)
        movies_poster.append(fetch_poster(movie_id))
    
    return recommend_movies, movies_poster

# Load data
movies_list = pickle.load(open('movies.pkl', 'rb'))
mlist = movies_list
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Select a movie to get recommendations',
    mlist['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)   
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx], use_container_width=True)
