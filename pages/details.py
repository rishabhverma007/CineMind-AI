import streamlit as st
from utils.api import client, poster
from utils.database import toggle_favourite


def render(movie_id: int):
    api = client(); movie = api.details(movie_id)
    if not movie:
        st.error("Movie details are unavailable. Check your TMDB API connection."); return
    if st.button("← Back to discovery"): st.session_state.pop("selected_movie", None); st.rerun()
    poster_col, info = st.columns([1, 2.3])
    with poster_col: st.image(poster(movie.get("poster_path")), use_container_width=True)
    with info:
        st.markdown(f"<div class='eyebrow'>{movie.get('release_date','')[:4]} · {movie.get('runtime','—')} min</div><h1>{movie.get('title')}</h1><h3 style='color:#fcd34d'>★ {movie.get('vote_average',0):.1f}/10</h3><p class='muted'>{movie.get('overview','No synopsis available.')}</p>", unsafe_allow_html=True)
        st.markdown(" ".join(f"<span class='tag'>{g['name']}</span>" for g in movie.get("genres", [])), unsafe_allow_html=True)
        x,y=st.columns(2)
        if x.button("♡ Save to library", use_container_width=True): st.toast("Saved" if toggle_favourite(movie) else "Removed")
        trailers = [v for v in movie.get("videos",{}).get("results",[]) if v.get("site")=="YouTube" and v.get("type")=="Trailer"]
        if trailers: y.link_button("Watch trailer ↗", f"https://www.youtube.com/watch?v={trailers[0]['key']}", use_container_width=True)
    credits = movie.get("credits", {})
    cast = credits.get("cast", [])[:8]
    director = next((p["name"] for p in credits.get("crew", []) if p.get("job")=="Director"), "—")
    st.markdown(f"### Credits\n**Director:** {director}")
    if cast: st.write(" · ".join(p["name"] for p in cast))
    providers = movie.get("watch/providers",{}).get("results",{}).get("IN", {}).get("flatrate", [])
    if providers: st.markdown("### Streaming on"); st.write(" · ".join(p["provider_name"] for p in providers))
    reviews = movie.get("reviews",{}).get("results",[])[:2]
    if reviews:
        st.markdown("### Viewer notes")
        for r in reviews: st.markdown(f"<div class='glass'><b>{r.get('author','Anonymous')}</b><br>{r.get('content','')[:500]}…</div><br>", unsafe_allow_html=True)
