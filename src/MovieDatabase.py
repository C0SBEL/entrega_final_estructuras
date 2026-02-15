import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class MovieDatabase:

    def __init__(self, uri=None, db_name=None):

        uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("MONGO_DB", "tmdb_movies_db")

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        try:
            self.client.server_info()
        except ServerSelectionTimeoutError as e:
            raise ConnectionError(f"No se puede conectar a MongoDB: {e}")

        self.db = self.client[db_name]

        # Colecciones
        self.movies = self.db.movies
        self.genres = self.db.genres
        self.production_companies = self.db.production_companies
        self.production_countries = self.db.production_countries
        self.languages = self.db.languages

        # ----------- ÍNDICES mínimos útiles -----------

        # Evitar duplicados de películas por id externo
        self.movies.create_index("id", unique=True)

        # Dimensiones: evitar duplicados en los ids
        self.genres.create_index("genre_id", unique=True)
        self.production_companies.create_index("company_id", unique=True)
        self.production_countries.create_index("country_id", unique=True)
        self.languages.create_index("language_id", unique=True)

    def insert_movies(self, docs, overwrite=False):

        if overwrite:
            self.movies.delete_many({})

        existing_ids = {
            doc["id"]
            for doc in self.movies.find({}, {"id": 1})
        }

        new_docs = [doc for doc in docs if doc["id"] not in existing_ids]

        if not new_docs:
            return 0

        result = self.movies.insert_many(new_docs)
        return len(result.inserted_ids)
