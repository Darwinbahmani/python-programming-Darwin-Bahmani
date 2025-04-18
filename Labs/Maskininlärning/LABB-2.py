import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


movies = pd.read_csv("ml-latest/movies.csv")
ratings = pd.read_csv("ml-latest/ratings.csv")

# Räkna ut medelbetyg per film
mean_ratings = ratings.groupby("movieId")["rating"].mean().reset_index()
mean_ratings.columns = ["movieId", "mean_rating"]

# Förbered genres
movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))
genres_encoded = movies["genres"].str.join('|').str.get_dummies(sep='|')

# Lägg till betygsinformation
movies = pd.merge(movies, mean_ratings, on="movieId", how="left")

# Genrefeatures
genre_features = genres_encoded

# Träna KNN
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(genre_features)

# Rekommendationsfunktion
def rekommendera_fem_filmer(filmtitel):
    match = movies[movies["title"].str.contains(filmtitel, case=False, na=False)]

    if match.empty:
        print(f"\n🚫 Ingen film hittades med titeln: {filmtitel}")
        return

    film_index = match.index[0]
    film_title = movies.loc[film_index, 'title']
    film_rating = movies.loc[film_index, 'mean_rating']

    film_feature = genre_features.iloc[film_index].values.reshape(1, -1)
    distances, indices = knn_model.kneighbors(film_feature, n_neighbors=50)

    # Ta bort originalfilmen från resultaten
    liknande_indices = [idx for idx in indices[0] if idx != film_index]
    liknande_filmer = movies.iloc[liknande_indices].copy()

    liknande_filmer["betygsskillnad"] = np.abs(liknande_filmer["mean_rating"] - film_rating)
    rekommenderade = liknande_filmer.sort_values("betygsskillnad").head(5)

    print(f"\n🎬 Rekommenderade filmer som liknar \"{film_title}\" (betyg: {round(film_rating, 2)}):")
    for _, row in rekommenderade.iterrows():
        print(f"- {row['title']} (betyg: {round(row['mean_rating'], 2)})")

# Kör interaktivt
if __name__ == "__main__":
    print("🔍 Skriv in en film:")
    filmtitel = input("> ")
    rekommendera_fem_filmer(filmtitel)
