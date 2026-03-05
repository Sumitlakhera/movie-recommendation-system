import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load saved model files
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations

@app.route("/recommend", methods=["GET"])
def recommend_movies():

    movie = request.args.get("movie")

    if movie not in movies["title"].values:
        return jsonify({"error": "Movie not found"}), 404

    recommendations = recommend(movie)

    return jsonify({
        "input_movie": movie,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)