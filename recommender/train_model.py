import pickle

from engine import build_dataset, create_vectors, compute_similarity

movies = build_dataset()

vectors = create_vectors(movies)

similarity = compute_similarity(vectors)

pickle.dump(movies, open("movies.pkl", "wb"))

pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Training on movies:", len(movies))
print(movies.columns)
print("Model saved successfully.")
