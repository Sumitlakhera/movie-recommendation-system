import requests
import pandas as pd
import time

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


def fetch_movie_metadata(movie_id, retries=3):

    for attempt in range(retries):

        try:
            url = f"{BASE_URL}/movie/{movie_id}"

            params = {
                "api_key": TMDB_API_KEY,
                "append_to_response": "credits,keywords"
            }

            response = session.get(url, params=params, timeout=20)

            if response.status_code != 200:
                time.sleep(1)
                continue

            data = response.json()

            return {
                "genres": data.get("genres", []),
                "cast": data.get("credits", {}).get("cast", []),
                "crew": data.get("credits", {}).get("crew", []),
                "keywords": data.get("keywords", {}).get("keywords", []),

                "popularity": data.get("popularity", 0),
                "vote_average": data.get("vote_average", 0),
                "vote_count": data.get("vote_count", 0),
                "release_date": data.get("release_date", "")
            }

        except Exception as e:
            print(f"Retry {attempt+1} failed for {movie_id}: {e}")
            time.sleep(2)

    return None


def enrich_movies():

    df = pd.read_csv("data/tmdb_new_movies_basic.csv")

    enriched_movies = []

    for i, row in df.iterrows():

        movie_id = int(row["movie_id"])

        print(f"Fetching metadata for {row['title']}")

        metadata = fetch_movie_metadata(movie_id)

        if not metadata:
            continue

        enriched_movies.append({
            "movie_id": movie_id,
            "title": row["title"],
            "overview": row["overview"],
            "genres": metadata["genres"],
            "keywords": metadata["keywords"],
            "cast": metadata["cast"],
            "crew": metadata["crew"],
            "popularity": metadata["popularity"],
            "vote_average": metadata["vote_average"],
            "vote_count": metadata["vote_count"],
            "release_date": metadata["release_date"]
        })

        time.sleep(1.2)

    enriched_df = pd.DataFrame(enriched_movies)

    enriched_df.to_csv("data/tmdb_new_movies_full.csv", index=False)

    print("Saved enriched dataset to data/tmdb_new_movies_full.csv")


if __name__ == "__main__":

    enrich_movies()