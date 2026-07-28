import streamlit as st
from components.movie_card import movie_grid
from utils.api import client
from utils.recommender import recommend, mood_rank, MOODS


def _catalog():
    api = client()
    return api.popular() + api.top_rated() + api.trending()


def recommendations(genre_map):
    st.title("AI Recommendations")
    st.caption("A transparent hybrid ranking of plot language, genre overlap, popularity and community ratings.")
    catalog = _catalog()
    if not catalog:
        st.info("Connect TMDB to generate a live recommendation set."); return
    titles = {f"{m['title']} ({(m.get('release_date') or '')[:4]})": m for m in catalog}
    selected = st.selectbox("Pick a film you enjoyed", list(titles))
    limit = st.slider("Recommendation count", 5, 20, 10)
    seed = titles[selected]
    st.markdown(f"<div class='glass'><b>Why this works</b><br><span class='muted'>CineMind compares story descriptions with TF-IDF, then blends in genre affinity, popularity and audience ratings.</span></div>", unsafe_allow_html=True)
    results = recommend(seed, catalog, limit)
    movie_grid(results, "recs", genre_map)
    if results:
        st.markdown("### Ranking explanation")
        for item in results[:5]: st.caption(f"**{item['title']} — {item['score']}% match.** {item['reason']}")


def mood(genre_map):
    st.title("Mood cinema")
    st.caption("Tell CineMind how you want to feel; it will tune discovery around that energy.")
    choice = st.select_slider("Your current mood", options=list(MOODS), value="Relaxing")
    st.markdown(f"<div class='glass'><span class='eyebrow'>Mood selected</span><h2>{choice}</h2><span class='muted'>A curated blend of {MOODS[choice]}.</span></div>", unsafe_allow_html=True)
    movie_grid(mood_rank(choice, _catalog()), f"mood_{choice}", genre_map)


def collection(title, getter, genre_map):
    st.title(title)
    movie_grid(getter(), title.lower().replace(' ', '_'), genre_map)
