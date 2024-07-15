import streamlit as st
import pickle
import pandas as pd
import requests
import re

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def normalize_title(title):
    title = title.lower()
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'[^\w\s]', '', title)
    return title.strip()


def fetch_poster(movie_title):
    api_key = '3054ad64'
    normalized_title = normalize_title(movie_title)
    response = requests.get(f'http://www.omdbapi.com/?t={normalized_title}&apikey={api_key}')
    data = response.json()

    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        response = requests.get(f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}')
        data = response.json()
        if 'Poster' in data and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return 'https://via.placeholder.com/500x750?text=No+Poster+Available'


def recommend(movie):
    movie_index = movies_list[movies_list['title'].values == movie].index[0]
    dist = similarity[movie_index]
    movies = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])
    movies = movies[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies:
        movie_title = movies_list.iloc[i[0]].title
        recommend_movies.append(movie_title)
        recommend_movies_posters.append(fetch_poster(movie_title))
    return recommend_movies, recommend_movies_posters


st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie', movies_list['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
            search_query = names[i].replace(' ', '+')
            download_link = f'https://9xflix.network/m/?s={search_query}'
            st.markdown(f'<a href="{download_link}" target="_blank">Download {names[i]}</a>', unsafe_allow_html=True)
