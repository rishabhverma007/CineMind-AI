import streamlit as st
from components.movie_card import movie_grid
from views import home, discover, analytics, details
from utils.api import client
from utils.database import favourites
from utils.style import inject_styles

st.set_page_config(page_title="CineMind AI", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")
inject_styles()

GENRES = {28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime", 18: "Drama", 14: "Fantasy", 27: "Horror", 9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 53: "Thriller", 10751: "Family"}

with st.sidebar:
    st.markdown("<h2>◉ CineMind <span style='color:#E50914'>AI</span></h2><p class='muted'>Your intelligent cinema guide</p>", unsafe_allow_html=True)
    page = st.radio("Navigate", ["Home", "Trending", "AI Recommendations", "Mood Recommendation", "Top Rated", "Upcoming", "Saved Movies", "Analytics"], label_visibility="collapsed")
    st.divider()
    st.markdown("<span class='eyebrow'>Preferences</span>", unsafe_allow_html=True)
    st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu", "Korean", "Japanese"])
    st.toggle("Motion effects", value=True)
    if not client().available:
        st.caption("Offline MovieLens mode")

if "selected_movie" in st.session_state:
    details.render(st.session_state.selected_movie)
elif page == "Home": home.render(GENRES)
elif page == "Trending": discover.collection("Trending this week", lambda: client().trending(), GENRES)
elif page == "AI Recommendations": discover.recommendations(GENRES)
elif page == "Mood Recommendation": discover.mood(GENRES)
elif page == "Top Rated": discover.collection("Top rated", lambda: client().top_rated(), GENRES)
elif page == "Upcoming": discover.collection("Coming soon", lambda: client().upcoming(), GENRES)
elif page == "Saved Movies":
    st.title("Your saved movies")
    st.caption("Your personal watchlist, stored privately on this device.")
    movie_grid(favourites(), "saved", GENRES)
elif page == "Analytics": analytics.render()

st.markdown("<br><div class='muted' style='text-align:center;font-size:.8rem'>Made with ♥ using Streamlit · TMDB · Scikit-learn</div>", unsafe_allow_html=True)
