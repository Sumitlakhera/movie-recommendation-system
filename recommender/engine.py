import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import load_datasets, merge_datasets, select_features, extract_features, create_tags


def build_dataset():

    movies, credits = load_datasets()

    movies = merge_datasets(movies, credits)

    movies = select_features(movies)

    movies = extract_features(movies)

    movies = create_tags(movies)

    return movies


def create_vectors(movies):

    tfidf = TfidfVectorizer(
        max_features=8000,
        stop_words="english",
        ngram_range=(1,2)
    )

    vectors = tfidf.fit_transform(movies["tags"]).toarray()

    return vectors


def compute_similarity(vectors):

    similarity = cosine_similarity(vectors)

    return similarity


def recommend(movie, movies, similarity):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movies_list:
        print(movies.iloc[i[0]].title)


if __name__ == "__main__":

    movies = build_dataset()

    vectors = create_vectors(movies)

    similarity = compute_similarity(vectors)

    recommend("Interstellar", movies, similarity)