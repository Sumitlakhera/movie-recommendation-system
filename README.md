# Movie Recommendation System

A content-based movie recommendation web application built with a Flask backend and a lightweight React frontend. The system recommends similar movies using metadata such as overview, genres, keywords, cast, crew, popularity, rating, and release date.

## Overview

This project helps users discover movies by entering a title and receiving a short list of related recommendations. It combines a trained similarity model with live movie metadata from The Movie Database (TMDB) to display posters, trending titles, and additional movie details.

## Features

- Search for a movie by title
- Get top movie recommendations based on content similarity
- View posters and basic movie details
- Browse trending movies
- Fetch trailers and extra metadata from TMDB
- Rebuild the dataset and similarity model from source data

## Tech Stack

- Backend: Flask, Flask-CORS
- Frontend: React 18 (CDN), HTML, CSS
- Data and ML: Pandas, scikit-learn, NLTK
- External API: TMDB

## Project Structure

```text
movie-recommendation-system/
├── backend/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── recommender/
│   ├── preprocess.py
│   ├── engine.py
│   ├── train_model.py
│   ├── fetch_tmdb_movies.py
│   ├── enrich_tmdb_movies.py
│   ├── enrich_old_movies.py
│   └── merge_datasets.py
├── data/
├── movies.pkl
├── similarity.pkl
└── requirements.txt
```

## How It Works

1. Movie data is prepared and transformed into weighted text tags.
2. A TF-IDF vectorizer converts those tags into numeric vectors.
3. Cosine similarity is used to compare movies.
4. Recommendation scores are refined with metadata such as genre overlap, keyword overlap, popularity, rating, votes, and recency.
5. TMDB is used at runtime for posters, trending movies, and trailers.

## Requirements

- Python 3.10+ recommended
- A TMDB API key

## Setup

1. Clone the repository and move into the project folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Add your TMDB API key to a `.env` file.

Example:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

## Run the Application

Start the backend from the project root:

```bash
python backend/app.py
```

Then open the frontend in your browser:

```bash
open frontend/index.html
```

If `open` is not available on your system, open `frontend/index.html` manually in a browser.

The frontend is currently configured to call the backend at:

```text
http://127.0.0.1:5000
```

## Rebuild the Model

Pretrained files `movies.pkl` and `similarity.pkl` are already present in the repository. If you want to retrain the model:

```bash
python recommender/train_model.py
```

This generates:

- `movies.pkl`
- `similarity.pkl`

## Rebuild or Expand the Dataset

The project also includes scripts for dataset preparation:

- `recommender/fetch_tmdb_movies.py` fetches newer movie records from TMDB
- `recommender/enrich_tmdb_movies.py` enriches fetched movies with metadata
- `recommender/merge_datasets.py` combines classic and newly fetched datasets
- `recommender/preprocess.py` cleans and prepares the final dataset for training

These scripts are useful if you want to refresh or expand the recommendation catalog.

## API Endpoints

The Flask backend exposes the following routes:

- `GET /recommend?movie=<title>` returns recommendations for a movie
- `GET /search?query=<text>` returns title suggestions
- `GET /movie-details?id=<movie_id>` returns movie details
- `GET /trending` returns trending movies
- `GET /trailer?id=<movie_id>` returns a YouTube trailer URL when available

## Notes

- The backend expects `movies.pkl` and `similarity.pkl` in the project root.
- TMDB-powered features require a valid API key.
- Some data generation scripts write CSV files inside the `data/` directory.

## Future Improvements

- Deploy the frontend and backend together
- Add filtering by genre, year, or rating
- Improve error handling and loading states
- Add tests and API documentation

## License

This project is intended for educational and portfolio use unless you add a separate license file.
