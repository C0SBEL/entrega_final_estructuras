from src.etl import extract, transform, load
from src.MovieDatabase import MovieDatabase


def run_pipeline():

    db = MovieDatabase()

    df_raw = extract()
    movies, genres, companies, countries, languages = transform(df_raw)

    load(movies, genres, companies, countries, languages, db)

    print("ETL completat.")


if __name__ == "__main__":
    run_pipeline()