import os
import requests
import streamlit as st
from dotenv import load_dotenv
from utils import local_data

load_dotenv()


def _tmdb_key() -> str:
    """Read a local .env key or the root-level Streamlit Cloud secret."""
    local_key = os.getenv("TMDB_API_KEY", "").strip()
    if local_key:
        return local_key
    try:
        if "TMDB_API_KEY" in st.secrets:
            return str(st.secrets["TMDB_API_KEY"]).strip()
    except Exception:
        pass
    return ""


class TMDBClient:
    def __init__(self):
        self.key = _tmdb_key()
        self.base = "https://api.themoviedb.org/3"

    @property
    def available(self):
        return bool(self.key)

    @st.cache_data(ttl=1800, show_spinner=False)
    def _get(_self, path: str, **params):
        if not _self.key:
            return None
        try:
            response = requests.get(f"{_self.base}{path}", params={**params, "api_key": _self.key}, timeout=12)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def trending(self, window="week"):
        return (self._get(f"/trending/movie/{window}") or {}).get("results", []) if self.available else local_data.popular()

    def popular(self):
        return (self._get("/movie/popular") or {}).get("results", []) if self.available else local_data.popular()

    def top_rated(self):
        return (self._get("/movie/top_rated") or {}).get("results", []) if self.available else local_data.top_rated()

    def upcoming(self):
        return (self._get("/movie/upcoming") or {}).get("results", []) if self.available else local_data.popular()

    def search(self, query):
        return (self._get("/search/movie", query=query, include_adult="false") or {}).get("results", []) if self.available else local_data.search(query)

    def details(self, movie_id):
        return self._get(f"/movie/{movie_id}", append_to_response="credits,videos,reviews,watch/providers") or {}


def client() -> TMDBClient:
    """Create a fresh lightweight client so Cloud Secrets changes take effect immediately."""
    return TMDBClient()


def poster(path: str | None, size="w500") -> str:
    return f"https://image.tmdb.org/t/p/{size}{path}" if path else "https://placehold.co/500x750/171720/94A3B8?text=CineMind"
