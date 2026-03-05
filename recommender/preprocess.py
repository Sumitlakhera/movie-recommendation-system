import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def load_datasets():

    movies = pd.read_csv("data/tmdb_5000_movies.csv")
    credits = pd.read_csv("data/tmdb_5000_credits.csv")

    return movies, credits


def merge_datasets(movies, credits):

    movies = movies.merge(credits, on="title")

    return movies


def select_features(movies):

    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)
    return movies


def convert(text):

    result = []

    for i in ast.literal_eval(text):
        result.append(i['name'])

    return result


def convert_cast(text):

    result = []

    counter = 0

    for i in ast.literal_eval(text):

        if counter < 3:
            result.append(i['name'])
            counter += 1
        else:
            break

    return result


def fetch_director(text):

    result = []

    for i in ast.literal_eval(text):

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
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
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