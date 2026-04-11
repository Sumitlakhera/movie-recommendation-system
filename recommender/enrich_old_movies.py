import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")   # <-- put your key here
BASE_URL = "https://api.themoviedb.org/3"

session = requests.Session()


def fetch_metadata(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}"

        params = {
            "api_key": TMDB_API_KEY
        }

        response = session.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"Failed {movie_id}: {response.status_code}")
            return None

        data = response.json()

        return {
            "movie_id": movie_id,
            "popularity": data.get("popularity", 0),
            "vote_average": data.get("vote_average", 0),
            "vote_count": data.get("vote_count", 0),
            "release_date": data.get("release_date", "")
        }

    except Exception as e:
        print(f"Error {movie_id}: {e}")
        return None


def enrich_old():

    print("Loading old dataset...")
    movies = pd.read_csv("data/tmdb_5000_movies.csv")

    movie_ids = movies["id"].tolist()

    results = []

    print(f"Fetching metadata for {len(movie_ids)} movies...\n")

    # 🔥 Parallel execution
    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [executor.submit(fetch_metadata, mid) for mid in movie_ids]

        for i, future in enumerate(as_completed(futures)):

            result = future.result()

            if result:
                results.append(result)

            # progress log
            if i % 100 == 0:
                print(f"Processed {i} movies")

    df = pd.DataFrame(results)

    df.to_csv("data/tmdb_old_movies_metadata.csv", index=False)

    print("\n✅ Saved old metadata to data/tmdb_old_movies_metadata.csv")


# ✅ MAIN ENTRY POINT
if __name__ == "__main__":
    enrich_old()