"""Offline MovieLens catalogue and collaborative-rating helpers."""
from pathlib import Path
from difflib import get_close_matches
import pandas as pd
import streamlit as st

try:
    from rapidfuzz import fuzz, process
except ImportError:
    fuzz = process = None

DATA_DIR = Path(__file__).resolve().parent.parent / "dataset" / "ml-latest-small"


@st.cache_data(show_spinner=False)
def catalogue() -> list[dict]:
    """Return MovieLens titles enriched with community-rating signals."""
    movies_path, ratings_path = DATA_DIR / "movies.csv", DATA_DIR / "ratings.csv"
    if not movies_path.exists() or not ratings_path.exists():
        return []
    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path).groupby("movieId").agg(vote_average=("rating", "mean"), vote_count=("rating", "size")).reset_index()
    data = movies.merge(ratings, on="movieId", how="left").fillna({"vote_average": 0, "vote_count": 0})
    data["title"] = data["title"].str.replace(r"\s*\(\d{4}\)$", "", regex=True)
    data["release_date"] = movies["title"].str.extract(r"\((\d{4})\)")[0].fillna("")
    data["popularity"] = data.vote_count.astype(float)  # Rating volume is the offline popularity proxy.
    data["genre_names"] = data.genres.replace("(no genres listed)", "").str.split("|")
    data["overview"] = data.apply(lambda row: f"{row['title']} is a {', '.join(row['genre_names'])} film.", axis=1)
    data = data.rename(columns={"movieId": "id"})
    return data[["id", "title", "genres", "genre_names", "release_date", "vote_average", "vote_count", "popularity", "overview"]].to_dict("records")


def search(query: str, limit: int = 20) -> list[dict]:
    items = catalogue()
    if not query.strip() or not items:
        return []
    titles = [item["title"] for item in items]
    if process:
        matches = process.extract(query, titles, scorer=fuzz.WRatio, limit=limit, score_cutoff=35)
        return [items[index] for _, _, index in matches]
    matched_titles = get_close_matches(query, titles, n=limit, cutoff=.28)
    return [next(item for item in items if item["title"] == title) for title in matched_titles]


def top_rated(limit: int = 30) -> list[dict]:
    return sorted((m for m in catalogue() if m["vote_count"] >= 20), key=lambda m: (m["vote_average"], m["vote_count"]), reverse=True)[:limit]


def popular(limit: int = 30) -> list[dict]:
    return sorted(catalogue(), key=lambda m: m["vote_count"], reverse=True)[:limit]
