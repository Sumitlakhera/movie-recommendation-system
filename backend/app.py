import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

TMDB_API_KEY = "6a81b7e4a3680f5b37a647ccf3726035"

app = Flask(__name__)
CORS(app)

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

        poster = fetch_poster(title)

        recommendations.append({
        "title": title,
        "poster": poster
    })

    return recommendations

def fetch_poster(movie_title):

    try:

        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"

        response = requests.get(url, timeout=5)

        data = response.json()

        if data.get("results"):

            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception as e:
        print("TMDB error:", e)

    return ""

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

if __name__ == "__main__":
    app.run(debug=True)