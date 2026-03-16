import requests
import pandas as pd
import time
import os

session = requests.Session()

session.headers.update({
    "accept": "application/json",
    "User-Agent": "movie-recommender-dataset-builder"
})

TMDB_API_KEY = "6a81b7e4a3680f5b37a647ccf3726035"

TMDB_HEADERS = {
    "accept": "application/json",
    "User-Agent": "movie-recommender-dataset-builder"
}

BASE_URL = "https://api.themoviedb.org/3"


def load_existing_movie_ids():

    existing_ids = set()

    if os.path.exists("data/combined_movies.csv"):

        df = pd.read_csv("data/combined_movies.csv")
        existing_ids = set(df["movie_id"].tolist())

        print(f"Loaded {len(existing_ids)} existing movies")

    return existing_ids


def fetch_movies(start_year=2017, end_year=2024, pages=15):

    all_movies = []

    existing_ids = load_existing_movie_ids()

    skipped = 0

    for year in range(start_year, end_year + 1):

        print(f"\nFetching movies for year {year}")

        for page in range(1, pages + 1):

            print(f"Year {year} | Page {page}")

            url = f"{BASE_URL}/discover/movie"

            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "sort_by": "popularity.desc",
                "primary_release_year": year,
                "page": page
            }

            try:

                response = session.get(
                    url,
                    params=params,
                    timeout=20
                )

                if response.status_code != 200:
                    print("Request failed, skipping page")
                    continue

                data = response.json()
                results = data.get("results", [])

                if not results:
                    print("No more movies for this year")
                    break

                for movie in results:

                    movie_id = movie.get("id")

                    if movie_id in existing_ids:
                        skipped += 1
                        continue

                    all_movies.append({
                        "movie_id": movie_id,
                        "title": movie.get("title"),
                        "overview": movie.get("overview")
                    })

                time.sleep(0.25)

            except Exception as e:

                print("Connection error, retrying...", e)
                time.sleep(2)
                continue

    print("\nSkipped existing movies:", skipped)
    print("New movies fetched:", len(all_movies))

    return pd.DataFrame(all_movies)


if __name__ == "__main__":

    df = fetch_movies(pages=50)

    print("Movies fetched:", len(df))

    df.to_csv("data/tmdb_new_movies_basic.csv", index=False)

    print("Saved to data/tmdb_new_movies_basic.csv")