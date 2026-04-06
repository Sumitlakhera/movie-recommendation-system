import pandas as pd
import json

# Load original datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")

# Keep only columns used in preprocessing
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# Load new enriched dataset
new_movies = pd.read_csv("data/tmdb_new_movies_full.csv")


# Convert Python lists → JSON strings
def convert_to_json(value):

    try:
        parsed = eval(value)

        return json.dumps(parsed)

    except:
        return json.dumps([])


for column in ["genres", "keywords", "cast", "crew"]:

    new_movies[column] = new_movies[column].apply(convert_to_json)


# Match original dataset structure
new_movies = new_movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# Combine datasets
combined = pd.concat([movies, new_movies], ignore_index=True)


# Remove duplicates
combined = combined.drop_duplicates(subset="movie_id")


print("Original movies:", len(movies))
print("New movies:", len(new_movies))
print("Combined dataset:", len(combined))


combined.to_csv("data/combined_movies.csv", index=False)

print("Saved combined dataset to data/combined_movies.csv")