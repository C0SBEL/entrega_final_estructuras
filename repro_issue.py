import polars as pl
from src.etl import transform

def test_duplicates():
    # Create a dummy DataFrame with duplicate IDs
    data = {
        "id": [1, 2, 1],
        "title": ["Movie 1", "Movie 2", "Movie 1 Dupe"],
        "original_title": ["M1", "M2", "M1D"],
        "release_date": ["2023-01-01", "2023-01-02", "2023-01-01"],
        "vote_average": [7.0, 8.0, 7.0],
        "vote_count": [100, 200, 100],
        "popularity": [10.0, 20.0, 10.0],
        "runtime": [120, 90, 120],
        "genres": ["Action", "Comedy", "Action"],
        "production_companies": ["Co A", "Co B", "Co A"],
        "production_countries": ["US", "UK", "US"],
        "spoken_languages": ["en", "en", "en"],
        "original_language": ["en", "en", "en"],
        "revenue": [1000, 2000, 1000],
        "overview": ["O1", "O2", "O1"],
        "tagline": ["T1", "T2", "T1"],
        "adult": [False, False, False],
        "homepage": ["H1", "H2", "H1"],
        "budget": [500, 600, 500]
    }
    df = pl.DataFrame(data)
    
    movies, genres, companies, countries, languages = transform(df)
    
    print(f"Number of movies: {len(movies)}")
    print(f"Unique IDs: {movies['id'].n_unique()}")
    
    if len(movies) != movies["id"].n_unique():
        print("FAIL: Duplicate IDs found in transformed movies!")
    else:
        print("SUCCESS: No duplicate IDs in transformed movies.")

if __name__ == "__main__":
    test_duplicates()
