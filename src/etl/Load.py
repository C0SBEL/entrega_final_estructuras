import polars as pl

class Loader:
    """
    Class to load transformed data into a MongoDB database.

    This class receives Polars DataFrames (or LazyFrames), collects them if necessary,
    and inserts the data into the corresponding MongoDB collections.
    """

    def __init__(self, db):
        """
        Initializes the Loader with a MongoDB database instance.

        Parameters
        ----------
        db : MovieDatabase
            An instance of the MovieDatabase class representing the MongoDB connection.
        """
        self.db = db

    def load(self, movies, genres, companies, countries, languages):
        """
        Loads movies, genres, companies, countries, and languages into MongoDB.

        This method first collects any Polars LazyFrames into DataFrames, clears
        the existing collections in MongoDB, and then inserts the new data.

        Parameters
        ----------
        movies : polars.DataFrame or polars.LazyFrame
            DataFrame containing movies data.
        genres : polars.DataFrame or polars.LazyFrame
            DataFrame containing genres data.
        companies : polars.DataFrame or polars.LazyFrame
            DataFrame containing production companies data.
        countries : polars.DataFrame or polars.LazyFrame
            DataFrame containing production countries data.
        languages : polars.DataFrame or polars.LazyFrame
            DataFrame containing spoken languages data.

        Notes
        -----
        - Existing data in the collections will be deleted before inserting new data.
        - Uses the `to_dicts()` method from Polars to convert DataFrames to dictionaries
          for MongoDB insertion.
        """
        print("Loading data into MongoDB...")

        # Collect LazyFrames if necessary
        if isinstance(movies, pl.LazyFrame):
            movies = movies.collect()
        if isinstance(genres, pl.LazyFrame):
            genres = genres.collect()
        if isinstance(companies, pl.LazyFrame):
            companies = companies.collect()
        if isinstance(countries, pl.LazyFrame):
            countries = countries.collect()
        if isinstance(languages, pl.LazyFrame):
            languages = languages.collect()

        # Clear existing collections
        self.db.movies.delete_many({})
        self.db.genres.delete_many({})
        self.db.production_companies.delete_many({})
        self.db.production_countries.delete_many({})
        self.db.languages.delete_many({})

        # Insert new data
        self.db.movies.insert_many(movies.to_dicts())
        self.db.genres.insert_many(genres.to_dicts())
        self.db.production_companies.insert_many(companies.to_dicts())
        self.db.production_countries.insert_many(countries.to_dicts())
        self.db.languages.insert_many(languages.to_dicts())

        print("Data loaded successfully.")
