import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from sqlalchemy.util import generic_repr


class MovieDatabase:

    def __init__(self, uri=None, db_name=None):

        uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("MONGO_DB", "tmdb_movies_db")

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        try:
            self.client.server_info()
        except ServerSelectionTimeoutError as e:
            raise ConnectionError(f"No es pot connectar a MongoDB: {e}")

        self.db = self.client[db_name]

        if "movies" not in self.db.list_collection_names():
            self.db.create_collection("movies")

        self.movies = self.db.movies
        self.genres = self.db.genres
        self.production_companies = self.db.production_companies
        self.production_countries = self.db.production_countries

        # Índexs útils per consultes
        self.movies.create_index("title")
        self.movies.create_index("release_date")
        self.movies.create_index("genres")
        self.movies.create_index("vote_average")
        self.movies.create_index([("genres", 1), ("vote_average", -1)])
        self.genres.create_index("name")
        self.production_companies.create_index("name")
        self.production_countries.create_index("name")

        self.movies.create_index([
            ("title", "text"),
            ("genres", "text")
        ])

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
