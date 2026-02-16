from src.db.MovieDatabase import MovieDatabase
from src.etl.Extract import Extractor
from src.etl.Transform import Transformer
from src.etl.Load import Loader

def run_etl():
    # Database initialization
    db = MovieDatabase()

    # Extract
    extractor = Extractor()
    df_raw = extractor.extract(10000)  # Extract 10,000 rows for testing

    # Transform
    transformer = Transformer()
    movies, genres, companies, countries, languages = transformer.transform(df_raw)

    # Load
    loader = Loader(db)
    loader.load(movies, genres, companies, countries, languages)

    print("ETL completed successfully")

if __name__ == "__main__":
    run_etl()
