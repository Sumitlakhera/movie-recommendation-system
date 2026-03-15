import requests
import pandas as pd
import time

TMDB_API_KEY = "6a81b7e4a3680f5b37a647ccf3726035"

TMDB_HEADERS = {
    "accept": "application/json",
    "User-Agent": "movie-recommender-dataset-builder"
}

BASE_URL = "https://api.themoviedb.org/3"


def fetch_movies(pages=20):

    all_movies = []

    for page in range(1, pages + 1):

        print(f"Fetching page {page}")

        url = f"{BASE_URL}/discover/movie"

        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": page
        }

        try:

            response = requests.get(
                url,
                params=params,
                headers=TMDB_HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                print("Request failed, skipping page")
                continue

            data = response.json()
            results = data.get("results", [])

            for movie in results:

                all_movies.append({
                    "movie_id": movie.get("id"),
                    "title": movie.get("title"),
                    "overview": movie.get("overview")
                })

            time.sleep(0.25)  # avoid API rate limits

        except Exception as e:

            print("Connection error, retrying...", e)
            time.sleep(2)
            continue

    return pd.DataFrame(all_movies)


if __name__ == "__main__":

    df = fetch_movies(pages=50)

    print("Movies fetched:", len(df))

    df.to_csv("data/tmdb_new_movies_basic.csv", index=False)

    print("Saved to data/tmdb_new_movies_basic.csv")