import pandas as pd
import ast
import json
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def load_datasets():

    movies = pd.read_csv("data/combined_movies.csv")

    return movies, None


def merge_datasets(movies, credits):

    return movies


def select_features(movies):

    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)
    return movies


def convert(text):

    result = []

    try:
        data = json.loads(text)
    except:
        data = ast.literal_eval(text)

    for i in data:
        result.append(i['name'])

    return result


def convert_cast(text):

    result = []

    try:
        data = json.loads(text)
    except:
        data = ast.literal_eval(text)

    counter = 0

    for i in data:

        if counter < 3:
            result.append(i['name'])
            counter += 1
        else:
            break

    return result


def fetch_director(text):

    result = []

    try:
        data = json.loads(text)
    except:
        data = ast.literal_eval(text)

    for i in data:

        if i['job'] == 'Director':
            result.append(i['name'])
            break

    return result


def extract_features(movies):

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    movies['cast'] = movies['cast'].apply(convert_cast)

    movies['crew'] = movies['crew'].apply(fetch_director)

    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)

    return movies


def create_tags(movies):

    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    movies['weighted_tags'] = (
        movies['overview'] +
        movies['genres'] * 3 +
        movies['keywords'] * 2 +
        movies['cast'] * 2 +
        movies['crew'] * 3
    )

    movies['tags'] = movies['weighted_tags'].apply(lambda x: " ".join(x))

    movies['tags'] = movies['tags'].apply(lambda x: x.lower())

    movies['tags'] = movies['tags'].apply(stem)

    return movies

def collapse(text):

    result = []

    for i in text:
        result.append(i.replace(" ",""))

    return result

def stem(text):

    result = []

    for i in text.split():
        result.append(ps.stem(i))

    return " ".join(result)

if __name__ == "__main__":

    movies, credits = load_datasets()

    movies = merge_datasets(movies, credits)

    movies = select_features(movies)

    movies = extract_features(movies)

    movies = create_tags(movies)

    print(movies[['title','tags']].head())