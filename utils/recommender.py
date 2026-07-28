"""Local hybrid recommender for live TMDB result sets."""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOODS = {
    "Happy": "comedy family animation joyful uplifting feel good",
    "Sad": "drama emotional heartbreak reflective poignant",
    "Romantic": "romance love relationship passionate",
    "Action": "action adventure crime thriller explosive",
    "Relaxing": "family comedy animation calm nature",
    "Mind Blowing": "science fiction mystery thriller psychological",
    "Horror": "horror supernatural terrifying suspense",
    "Motivational": "inspiring biography sport triumph ambition",
}


def _text(movie: dict) -> str:
    return " ".join([movie.get("title", ""), movie.get("original_title", ""), movie.get("overview", ""), " ".join(movie.get("genre_names", []))])


def recommend(seed: dict, candidates: list[dict], limit=20) -> list[dict]:
    pool = [m for m in candidates if m.get("id") != seed.get("id")]
    if not pool: return []
    docs = [_text(seed)] + [_text(m) for m in pool]
    matrix = TfidfVectorizer(stop_words="english", max_features=3000).fit_transform(docs)
    content = cosine_similarity(matrix[0:1], matrix[1:])[0]
    seed_genres = set(seed.get("genre_ids", [])) | set(seed.get("genre_names", []))
    popularity = np.array([m.get("popularity", 0) for m in pool], dtype=float)
    ratings = np.array([m.get("vote_average", 0) for m in pool], dtype=float)
    norm = lambda x: (x-x.min())/(x.max()-x.min()+1e-9)
    genre = np.array([len(seed_genres & (set(m.get("genre_ids", [])) | set(m.get("genre_names", [])))) / max(1, len(seed_genres)) for m in pool])
    scores = .70*content + .15*genre + .10*norm(popularity) + .05*norm(ratings)
    ranked = []
    for movie, score, cscore, gscore in zip(pool, scores, content, genre):
        item = dict(movie); item["score"] = round(float(score)*100, 1)
        item["reason"] = f"{round(float(cscore)*100)}% story match" + (f" · shared genre affinity {round(float(gscore)*100)}%" if gscore else " · strong audience signals")
        ranked.append(item)
    return sorted(ranked, key=lambda x: x["score"], reverse=True)[:limit]


def mood_rank(mood: str, movies: list[dict], limit=20) -> list[dict]:
    terms = set(re.findall(r"\w+", MOODS.get(mood, mood).lower()))
    def score(m):
        words = set(re.findall(r"\w+", _text(m).lower()))
        return len(words & terms) * 10 + m.get("vote_average", 0) + m.get("popularity", 0)/100
    return sorted(movies, key=score, reverse=True)[:limit]
