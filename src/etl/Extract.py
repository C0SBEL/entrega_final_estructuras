import kagglehub
from kagglehub import KaggleDatasetAdapter

class Extractor:
    """
    Class to extract datasets from Kaggle using kagglehub.

    This class allows downloading a dataset in Polars format and optionally limits
    the number of rows for faster testing or prototyping.
    """

    def __init__(self, dataset="asaniczka/tmdb-movies-dataset-2023-930k-movies",
                 file="TMDB_movie_dataset_v11.csv"):
        """
        Initializes the Extractor with the dataset and file name.

        Parameters
        ----------
        dataset : str, optional
            Kaggle dataset identifier in the format 'username/dataset-name'.
            Default is 'asaniczka/tmdb-movies-dataset-2023-930k-movies'.
        file : str, optional
            CSV file name within the dataset to extract. Default is
            'TMDB_movie_dataset_v11.csv'.
        """
        self.dataset = dataset
        self.file = file

    def extract(self, limit=None):
        """
        Extracts the dataset and returns it as a Polars DataFrame.

        Parameters
        ----------
        limit : int, optional
            If provided, limits the number of rows returned (useful for testing).

        Returns
        -------
        polars.DataFrame
            The extracted dataset as a Polars DataFrame.

        Notes
        -----
        Uses kagglehub to load the dataset in Polars format.
        """
        print("Extracting data...")
        lf = kagglehub.dataset_load(
            KaggleDatasetAdapter.POLARS,
            self.dataset,
            self.file
        )
        if limit:
            lf = lf.limit(limit)
        return lf.collect()
