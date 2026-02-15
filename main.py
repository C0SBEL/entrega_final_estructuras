from src.etl import extract, transform, load
from src.MovieDatabase import MovieDatabase


def run_pipeline():

    db = MovieDatabase()

    df_raw = extract(limit=10000)
    movies, genres, companies, countries = transform(df_raw)

    load(movies, genres, companies, countries, db)

    print("ETL completat.")


if __name__ == "__main__":
    run_pipeline()