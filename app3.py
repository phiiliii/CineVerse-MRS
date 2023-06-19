import streamlit as st
import pickle
import pandas as pd
import requests
import random
import time

st.set_page_config(page_title='CineVerse', page_icon='🎬')

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2019/04/24/21/55/cinema-4153289_1280.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9e3b659c63585db7c27a32349bc2b1f0&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

    # Randomize the selection of movies
    random.shuffle(movies_list)

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_overview = []  # Store the movie overviews
    recommended_movies_ids = []  # Store the movie IDs
    for i in movies_list[:5]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster with API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_overview.append(movies.iloc[i[0]].summary)
        recommended_movies_ids.append(movie_id)
    return recommended_movies, recommended_movies_posters, recommended_movies_overview, recommended_movies_ids

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500&display=swap');

    body {
        font-family: 'Montserrat', Arial, sans-serif;
        color: #EAEAEA;
        background-image: url('https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.setaswall.com%2Fsolid-color-background-wallpapers%2Fpaynes-grey-solid-color-background-wallpaper-5120x2880%2F&psig=AOvVaw1RNMM_w13YrGbYXsTbuCue&ust=1687191539812000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCJj49bOczf8CFQAAAAAdAAAAABAE');  
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin: 40px 0;
        letter-spacing: -1px;
        color: #08D9D6;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }

    .recommendation-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }

    .movie-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px;
        text-align: center;
        background-color: rgb(37, 42, 52, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.8);
    }

    .movie-card img {
        width: 200px;
        height: 300px;
        object-fit: cover;
        border-radius: 10px;
    }

    .movie-card a {
        text-decoration: none;
        color: inherit;
    }

    .movie-card-title {
        font-size: 34px;
        font-weight: bold;
        margin-top: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #FF2E63;
        white-space: nowrap;
    }

    .movie-card-overview {
        font-size: 18px;
        margin-top: 10px;
        line-height: 1.4;
        max-height: 120px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('CineVerse 🎬')

selected_movie_name = st.selectbox(
    'Tell us a movie and we will recommend similar ones for you.',
    movies['title'].values,
    key='movie_select'
)

if st.button('Recommend', key='recommend_button'):
    names, posters, overviews, ids = recommend(selected_movie_name)

    progress_bar = st.progress(0)

    for perc_completed in range(100):
        time.sleep(0.01)
        progress_bar.progress(perc_completed + 1)

    if len(names) == 0:
        st.warning("You have reached the end of the recommendations.")
    else:
        st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
        for i in range(5):
            st.markdown(
                f'<div class="movie-card"><a href="https://www.themoviedb.org/movie/{ids[i]}" target="_blank">'
                f'<img src="{posters[i]}"></a><div class="movie-card-title">{names[i]}</div>'
                f'<div class="movie-card-overview">{overviews[i]}</div></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
