import kagglehub
from kagglehub import KaggleDatasetAdapter
import polars as pl


# ---------------- EXTRACT ----------------

def extract(limit=None):
    print("Extracting data...")

    lf = kagglehub.dataset_load(
        KaggleDatasetAdapter.POLARS,
        "asaniczka/tmdb-movies-dataset-2023-930k-movies",
        "TMDB_movie_dataset_v11.csv"
    )

    if limit:
        lf = lf.limit(limit)

    return lf.collect()


# ---------------- TRANSFORM ----------------

def transform(df: pl.DataFrame):

    print("Transforming data...")

    # ---------- base movies ----------
    movies = df.select([
        "id",
        "title",
        "release_date",
        "vote_average",
        "vote_count",
        "popularity",
        "runtime",
        "genres",
        "production_companies",
        "production_countries"
    ])

    # ---------- GENRES ----------
    genres = (
        df.select(pl.col("genres").str.split(", "))
        .explode("genres")
        .drop_nulls()
        .unique()
        .rename({"genres": "name"})
        .with_row_count("genre_id")
    )

    genre_map = dict(zip(genres["name"], genres["genre_id"]))

    movies = movies.with_columns(
        pl.col("genres")
        .str.split(", ")
        .map_elements(
            lambda x: [genre_map[g] for g in x if g in genre_map]
        )
        .alias("genre_ids")
    ).drop("genres")

    # ---------- PRODUCTION COMPANIES ----------
    companies = (
        df.select(pl.col("production_companies").str.split(", "))
        .explode("production_companies")
        .drop_nulls()
        .unique()
        .rename({"production_companies": "name"})
        .with_row_count("company_id")
    )

    company_map = dict(zip(companies["name"], companies["company_id"]))

    movies = movies.with_columns(
        pl.col("production_companies")
        .str.split(", ")
        .map_elements(
            lambda x: [company_map[c] for c in x if c in company_map]
        )
        .alias("company_ids")
    ).drop("production_companies")

    # ---------- PRODUCTION COUNTRIES ----------
    countries = (
        df.select(pl.col("production_countries").str.split(", "))
        .explode("production_countries")
        .drop_nulls()
        .unique()
        .rename({"production_countries": "name"})
        .with_row_count("country_id")
    )

    country_map = dict(zip(countries["name"], countries["country_id"]))

    movies = movies.with_columns(
        pl.col("production_countries")
        .str.split(", ")
        .map_elements(
            lambda x: [country_map[c] for c in x if c in country_map]
        )
        .alias("country_ids")
    ).drop("production_countries")

    return movies, genres, companies, countries


# ---------------- LOAD ----------------

def load(movies, genres, companies, countries, db):

    print("Loading to MongoDB...")

    db.movies.delete_many({})
    db.genres.delete_many({})
    db.production_companies.delete_many({})
    db.production_countries.delete_many({})

    db.movies.insert_many(movies.to_dicts())
    db.genres.insert_many(genres.to_dicts())
    db.production_companies.insert_many(companies.to_dicts())
    db.production_countries.insert_many(countries.to_dicts())

    print("Data loaded correctly.")