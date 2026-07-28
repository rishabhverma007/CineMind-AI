# Offline data

CineMind includes the official [MovieLens latest-small](https://grouplens.org/datasets/movielens/latest/) dataset in `dataset/ml-latest-small`.

- 9,742 movies
- 100,836 user ratings from 610 users
- Genre metadata and TMDB/IMDb links

The app calculates an average score and rating-volume popularity signal from this data. It uses the catalogue for fuzzy search and content-based recommendations whenever a TMDB key is not configured. Attribution and terms are in `dataset/ml-latest-small/README.txt`.
