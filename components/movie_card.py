import streamlit as st
from utils.api import poster
from utils.database import toggle_favourite


def movie_grid(movies: list[dict], key_prefix="movie", genre_map=None) -> None:
    if not movies:
        st.info("No films found. Try a different search or check your TMDB API key.")
        return
    for row_start in range(0, len(movies), 5):
        cols = st.columns(5)
        for col, movie in zip(cols, movies[row_start:row_start+5]):
            with col:
                title = movie.get("title") or movie.get("name", "Untitled")
                year = (movie.get("release_date") or "—")[:4]
                genres = movie.get("genre_names") or [genre_map.get(i, "") for i in movie.get("genre_ids", [])] if genre_map else movie.get("genre_names", [])
                chips = "".join(f'<span class="tag">{g}</span>' for g in genres[:2] if g)
                st.markdown(f'''<div class="movie-card"><img src="{poster(movie.get('poster_path'))}" alt="{title}"><div class="movie-copy"><div class="movie-title">{title}</div><span class="badge">★ {movie.get('vote_average', 0):.1f}</span> <span class="muted"> · {year}</span><br>{chips}</div></div>''', unsafe_allow_html=True)
                a, b = st.columns(2)
                if a.button("Details", key=f"{key_prefix}_details_{movie['id']}", use_container_width=True):
                    st.session_state.selected_movie = movie["id"]
                    st.rerun()
                if b.button("♡", key=f"{key_prefix}_save_{movie['id']}", use_container_width=True):
                    saved = toggle_favourite(movie)
                    st.toast("Saved to your library" if saved else "Removed from library")
