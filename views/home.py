import streamlit as st
from components.movie_card import movie_grid
from utils.api import client, poster
from utils.database import log_search


def render(genre_map):
    api = client()
    featured = api.trending() or api.popular()
    hero = featured[0] if featured else {"title": "Cinema, intelligently curated.", "overview": "Your offline catalogue is ready.", "backdrop_path": None}
    hero_bg = poster(hero.get("backdrop_path"), "original") if hero.get("backdrop_path") else "linear-gradient(120deg,#20133c,#073042)"
    st.markdown(f'''<section class="hero" style="--hero:url('{hero_bg}')"><div class="eyebrow">Cinemind intelligence</div><h1>{hero.get('title')}</h1><p style="max-width:560px;color:#d1d5db;font-size:1.05rem">{hero.get('overview','Discover stories selected for your next great watch.')}</p></section>''', unsafe_allow_html=True)
    query = st.text_input("Search movies", placeholder="Search a movie, actor, director, or an imperfect title…", label_visibility="collapsed")
    if query:
        log_search(query)
        st.markdown("<h2 class='section'>Search results</h2>", unsafe_allow_html=True)
        movie_grid(api.search(query), "search", genre_map)
        return
    if not api.available:
        st.info("Offline MovieLens mode is active — recommendations use 100,836 community ratings across 9,742 films. Add TMDB_API_KEY in Streamlit Secrets for posters, trailers and live TMDB discovery.")
    st.markdown("<h2 class='section'>Trending now</h2>", unsafe_allow_html=True)
    movie_grid(featured[:10], "trend", genre_map)
    st.markdown("<h2 class='section'>Top rated picks</h2>", unsafe_allow_html=True)
    movie_grid((api.top_rated() or api.popular())[:10], "top", genre_map)
