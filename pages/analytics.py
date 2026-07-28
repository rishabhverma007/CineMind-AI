import streamlit as st
from components.charts import charts
from utils.api import client


def render():
    st.title("Cinema analytics")
    st.caption("A visual read on the titles shaping the current movie conversation.")
    movies = client().popular() + client().trending()
    figures = charts(movies)
    if not figures:
        st.info("Connect TMDB to see live analytics."); return
    left, right = st.columns(2)
    left.plotly_chart(figures[0], use_container_width=True)
    right.plotly_chart(figures[1], use_container_width=True)
    avg = sum(m.get("vote_average", 0) for m in movies)/len(movies)
    a,b,c = st.columns(3); a.metric("Titles sampled", len(movies)); b.metric("Average rating", f"{avg:.1f}/10"); c.metric("Live source", "TMDB")
