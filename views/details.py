import html
import streamlit as st
from utils.api import client, poster
from utils.database import toggle_favourite
from utils.local_data import catalogue


def _text(value: object, fallback: str = "") -> str:
    """Safely render API and CSV values that may be missing or non-string."""
    return html.escape(str(value if value is not None else fallback))


def _offline_movie(movie_id: int) -> dict:
    return next((movie for movie in catalogue() if int(movie["id"]) == int(movie_id)), {})


def render(movie_id: int):
    api = client()
    movie = api.details(movie_id)
    offline = not bool(movie)
    if offline:
        movie = _offline_movie(movie_id)
    if not movie:
        st.error("Movie details could not be found.")
        return
    if st.button("← Back to discovery"):
        st.session_state.pop("selected_movie", None)
        st.rerun()
    poster_col, info = st.columns([1, 2.3])
    with poster_col:
        if movie.get("poster_path"):
            st.image(poster(movie["poster_path"]), use_container_width=True)
        else:
            st.markdown(f'''<div class="glass" style="min-height:340px;display:flex;align-items:flex-end;background:linear-gradient(145deg,#312e81,#0e7490);font-size:1.7rem;font-weight:800">{_text(movie.get('title'), 'CineMind')}</div>''', unsafe_allow_html=True)
    with info:
        runtime = movie.get("runtime") or "—"
        st.markdown(f"<div class='eyebrow'>{_text(movie.get('release_date', ''))[:4]} · {_text(runtime)} min</div><h1>{_text(movie.get('title'), 'Untitled')}</h1><h3 style='color:#fcd34d'>★ {float(movie.get('vote_average') or 0):.1f}/10</h3><p class='muted'>{_text(movie.get('overview'), 'No synopsis available.')}</p>", unsafe_allow_html=True)
        genres = movie.get("genres") or [{"name": genre} for genre in movie.get("genre_names", [])]
        genre_tags = " ".join(f"<span class='tag'>{_text(genre.get('name'))}</span>" for genre in genres if isinstance(genre, dict) and genre.get("name") is not None)
        st.markdown(genre_tags, unsafe_allow_html=True)
        if offline:
            st.info("Offline MovieLens details: add TMDB_API_KEY in Streamlit Secrets to unlock poster, trailer, cast, reviews, and streaming providers.")
        left, right = st.columns(2)
        if left.button("♡ Save to library", use_container_width=True):
            st.toast("Saved" if toggle_favourite(movie) else "Removed")
        trailers = [video for video in movie.get("videos", {}).get("results", []) if video.get("site") == "YouTube" and video.get("type") == "Trailer"]
        if trailers:
            right.link_button("Watch trailer ↗", f"https://www.youtube.com/watch?v={trailers[0]['key']}", use_container_width=True)
    if offline:
        return
    credits = movie.get("credits", {})
    cast = credits.get("cast", [])[:8]
    director = next((person["name"] for person in credits.get("crew", []) if person.get("job") == "Director"), "—")
    st.markdown(f"### Credits\n**Director:** {director}")
    if cast:
        st.write(" · ".join(person["name"] for person in cast))
    providers = movie.get("watch/providers", {}).get("results", {}).get("IN", {}).get("flatrate", [])
    if providers:
        st.markdown("### Streaming on")
        st.write(" · ".join(provider["provider_name"] for provider in providers))
    reviews = movie.get("reviews", {}).get("results", [])[:2]
    if reviews:
        st.markdown("### Viewer notes")
        for review in reviews:
            st.markdown(f"<div class='glass'><b>{_text(review.get('author'), 'Anonymous')}</b><br>{_text(str(review.get('content', ''))[:500])}…</div><br>", unsafe_allow_html=True)
