import pandas as pd
import json

# Load original datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")
old_meta = pd.read_csv("data/tmdb_old_movies_metadata.csv")

#merger credits
movies = movies.merge(credits[['title','cast','crew']], on="title")

movies = movies.rename(columns={"id": "movie_id"})

#debug
print("Before meta merge:", movies.columns.tolist())

#merge metadata using TMDB id
movies = movies.merge(
    old_meta,
    on="movie_id",
    how="left",
    suffixes=("", "_meta")
)

# overwrite original columns with metadata
movies["popularity"] = movies["popularity_meta"]
movies["vote_average"] = movies["vote_average_meta"]
movies["vote_count"] = movies["vote_count_meta"]
movies["release_date"] = movies["release_date_meta"]

# drop extra columns
movies = movies.drop(columns=[
    "popularity_meta",
    "vote_average_meta",
    "vote_count_meta",
    "release_date_meta"
])

# Keep only columns used in preprocessing
movies = movies[
    ['movie_id','title','overview','genres','keywords','cast','crew',
     'popularity','vote_average','vote_count','release_date']
]

print(movies.columns.tolist())


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
new_movies = new_movies[
    ['movie_id','title','overview','genres','keywords','cast','crew',
     'popularity','vote_average','vote_count','release_date']
]


# Combine datasets
combined = pd.concat([movies, new_movies], ignore_index=True)


# Remove duplicates
combined = combined.drop_duplicates(subset="movie_id")


print("Original movies:", len(movies))
print("New movies:", len(new_movies))
print("Combined dataset:", len(combined))
print(combined.columns)



combined.to_csv("data/combined_movies.csv", index=False)

print("Saved combined dataset to data/combined_movies.csv")