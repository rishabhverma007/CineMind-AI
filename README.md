# CineMind AI

A premium Streamlit movie discovery app powered by TMDB and a local hybrid recommendation engine.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add TMDB_API_KEY to .env
streamlit run app.py
```

The app works in a graceful demo mode without a TMDB key. Add a key for live posters, trailers, cast, providers, reviews, trending titles and movie details.

## Architecture

- `app.py`: application shell and navigation
- `components/`: reusable UI cards, hero, charts and styling
- `utils/api.py`: resilient, cached TMDB client
- `utils/recommender.py`: TF-IDF hybrid content recommender and mood search
- `utils/database.py`: SQLite favourites and activity history
- `pages/`: page renderers

Recommendation ranking combines normalized text similarity (70%), genre overlap (15%), popularity (10%) and ratings (5%). If `sentence-transformers` is available it is used for semantic reranking; the application otherwise remains fully functional with TF-IDF.
