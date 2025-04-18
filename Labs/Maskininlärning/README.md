# Filmrekommendationssystem – LABB 2, Maskininlärning VT24

Detta program är ett enkelt rekommendationssystem som rekommenderar filmer baserat på:
- **Genrelikhet** (via one-hot encoding + cosine similarity)
- **Liknande betyg** (medelbetyg från användare)

---

##  Metod

### 1. Featureval
- Genrer från `movies.csv` används som features.
- Genrerna one-hot-encodas (t.ex. Action, Comedy, Sci-Fi).
- För varje film räknas medelbetyg ut från `ratings.csv`.

### 2. Modell
- En **K-Nearest Neighbors**-modell tränas på genrerna.
- Vi använder **cosine similarity** som mått för genrelikhet.
- Programmet hämtar de 50 filmer som är mest lika i genre.
- Sedan filtreras de filmerna utifrån hur nära deras betyg ligger originalfilmens betyg.

---

##  Användning

Kör programmet via terminal:


python LABB-2.py
