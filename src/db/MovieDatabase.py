import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

class MovieDatabase:
    """
    Class to handle the connection and basic operations on the MongoDB database
    for the TMDB Movies Dataset.

    This class establishes a connection to MongoDB, creates references to the main
    collections (movies, genres, production_companies, production_countries, languages),
    and ensures that unique indexes exist for the identifier fields.
    """

    def __init__(self, uri=None, db_name=None):
        """
        Initializes the connection to MongoDB and sets up the project collections.

        Parameters
        ----------
        uri : str, optional
            MongoDB connection URI. If not provided, the environment variable 'MONGO_URI'
            is used, or 'mongodb://localhost:59130/' by default.
        db_name : str, optional
            Name of the database. If not provided, the environment variable 'MONGO_DB'
            is used, or 'tmdb_movies_db' by default.

        Raises
        ------
        ConnectionError
            Raised if the connection to MongoDB cannot be established within the timeout.
        """
        uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:59130/")
        db_name = db_name or os.getenv("MONGO_DB", "tmdb_movies_db")

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        try:
            self.client.server_info()
        except ServerSelectionTimeoutError as e:
            raise ConnectionError(f"Cannot connect to MongoDB: {e}")

        # References to collections
        self.db = self.client[db_name]
        self.movies = self.db.movies
        self.genres = self.db.genres
        self.production_companies = self.db.production_companies
        self.production_countries = self.db.production_countries
        self.languages = self.db.languages

        # Create unique indexes to ensure data consistency
        self.movies.create_index("id", unique=True)
        self.genres.create_index("genre_id", unique=True)
        self.production_companies.create_index("company_id", unique=True)
        self.production_countries.create_index("country_id", unique=True)
        self.languages.create_index("language_id", unique=True)
