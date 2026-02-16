import polars as pl

class Transformer:
    """
    Class to transform raw TMDB movies data into normalized Polars DataFrames.

    This class handles:
    - Selecting relevant columns from the raw dataset.
    - Normalizing multivalued fields such as genres, production companies,
      production countries, and spoken languages by mapping them to unique IDs.
    - Returning transformed LazyFrames for efficient further processing.
    """

    def __init__(self):
        """
        Initializes the Transformer.

        Currently, no parameters are needed. The transform logic is applied
        directly in the transform() method.
        """
        pass

    def transform(self, df: pl.DataFrame):
        """
        Transforms the raw Polars DataFrame into a normalized structure suitable
        for loading into MongoDB.

        Parameters
        ----------
        df : pl.DataFrame
            Raw Polars DataFrame containing the TMDB movies dataset.

        Returns
        -------
        tuple of pl.LazyFrame
            - movies: LazyFrame containing movie records with normalized IDs.
            - genres: LazyFrame containing unique genres with genre_id.
            - companies: LazyFrame containing unique production companies with company_id.
            - countries: LazyFrame containing unique production countries with country_id.
            - languages: LazyFrame containing unique spoken languages with language_id.

        Notes
        -----
        - Multi-valued fields are split and mapped to numeric IDs.
        - LazyFrames are returned to allow deferred evaluation and efficient processing.
        - Columns kept for movies: id, title, original_title, release_date, vote_average,
          vote_count, popularity, runtime, original_language, revenue, overview,
          tagline, adult, homepage, budget, genre_ids, company_ids, country_ids, language_ids.
        """
        print("Transforming data...")

        # Select relevant columns for movies
        movies = df.select([
            "id", "title", "original_title", "release_date", "vote_average",
            "vote_count", "popularity", "runtime", "genres",
            "production_companies", "production_countries", "spoken_languages",
            "original_language", "revenue", "overview", "tagline",
            "adult", "homepage", "budget"
        ]).lazy()

        # Transform genres
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
                lambda x: [genre_map[g] for g in x if g in genre_map],
                return_dtype=pl.List(pl.Int64)
            ).alias("genre_ids")
        ).drop("genres")

        # Transform production companies
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
                lambda x: [company_map[c] for c in x if c in company_map],
                return_dtype=pl.List(pl.Int64)
            ).alias("company_ids")
        ).drop("production_companies")

        # Transform production countries
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
                lambda x: [country_map[c] for c in x if c in country_map],
                return_dtype=pl.List(pl.Int64)
            ).alias("country_ids")
        ).drop("production_countries")

        # Transform spoken languages
        languages = (
            df.select(pl.col("spoken_languages").str.split(", "))
            .explode("spoken_languages")
            .drop_nulls()
            .unique()
            .rename({"spoken_languages": "name"})
            .with_row_count("language_id")
        )
        language_map = dict(zip(languages["name"], languages["language_id"]))
        movies = movies.with_columns(
            pl.col("spoken_languages")
            .str.split(", ")
            .map_elements(
                lambda x: [language_map[l] for l in x if l in language_map],
                return_dtype=pl.List(pl.Int64)
            ).alias("language_ids")
        ).drop("spoken_languages")

        return movies, genres, companies, countries, languages
