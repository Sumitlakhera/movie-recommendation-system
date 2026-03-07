import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

TMDB_API_KEY = "6a81b7e4a3680f5b37a647ccf3726035"

app = Flask(__name__)
CORS(app)

tmdb_cache = {}
poster_cache = {}

# Load saved model files
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):

    movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:

        title = movies.iloc[i[0]].title
        movie_id = int(movies.iloc[i[0]].movie_id)
        poster = fetch_poster(movie_id)

        recommendations.append({
          "title": title,
          "movie_id": movie_id,
          "poster": poster
       })

    return recommendations

def fetch_poster(movie_id):

    # Check poster cache first
    if movie_id in poster_cache:
        return poster_cache[movie_id]

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        poster_url = None
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        # Save result in cache
        poster_cache[movie_id] = poster_url

        return poster_url

    except Exception as e:
        print("TMDB poster error:", e)
        return None

def fetch_movie_details(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster = None
        if data.get("poster_path"):
            poster = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

        return {
            "title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date"),
            "rating": data.get("vote_average"),
            "poster": poster
        }

    except Exception as e:
        print("TMDB error:", e)
        return None

@app.route("/recommend", methods=["GET"])
def recommend_movies():

    movie = request.args.get("movie")

    match = movies[movies['title'].str.lower() == movie.lower()]

    if match.empty:
        return jsonify({"error": "Movie not found"}), 404

    movie_index = match.index[0]

    recommendations = recommend(movie)

    return jsonify({
        "input_movie": movie,
        "recommendations": recommendations
    })

@app.route("/search", methods=["GET"])
def search_movies():

    query = request.args.get("query")

    if not query:
        return jsonify([])

    matches = movies[
        movies["title"].str.lower().str.contains(query.lower())
    ]["title"].head(5)

    return jsonify(matches.tolist())

@app.route("/movie-details", methods=["GET"])
def movie_details():

    movie_id = request.args.get("id")

    # Check cache first
    if movie_id in tmdb_cache:
        return jsonify(tmdb_cache[movie_id])

    if not movie_id:
        return jsonify({"error": "No movie_id provided"}), 400

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

        response = requests.get(url, timeout=10)

        data = response.json()

        movie = data

        poster_path = movie.get("poster_path")

        poster_url = None
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        movie_data = {
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "poster": poster_url
        }

        # Save in cache
        tmdb_cache[movie_id] = movie_data

        return jsonify(movie_data)

    except Exception as e:
     print("Movie details error:", e)

     return jsonify({
        "title": "Unknown Movie",
        "overview": "Movie details are currently unavailable.",
        "release_date": "Unknown",
        "rating": "N/A",
        "poster": None
     })

print(movies.columns)
print(movies[['title','movie_id']].head(5))
if __name__ == "__main__":
    app.run(debug=True)