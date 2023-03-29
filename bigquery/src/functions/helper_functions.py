import typing
import logging

try:
    from google.cloud import bigquery
    import google.auth.exceptions as g_exceptions
except ImportError as e:
    logging.error(f"Failed to import the Google Cloud Python API. Please ensure that it's installed.")
    raise e

class BigQueryQuery:
    """
    Wrapper class around the actual query string.
    
    Provides an API surface that allows for additional methods to be implemented, such as checking of the query.
    """
    
    @staticmethod
    def validate_query(query_str: str) -> bool:
        if len(query_str) == 0:
            logging.error(f"Empty query passed!")
            return False
        return True
    
    def __init__(self, query_str: str, job_config: typing.Optional[bigquery.QueryJobConfig] = None) -> None:
        """
        Initializes the instance.

        Parameters
        ----------
        query_str : str
            Query string that will be used to query the BigQuery job.
        job_config: typing.Optional[bigquery.QueryJobConfig]
            QueryJobConfig type, used to configure the query parameters. By default None.

        Returns
        -------
        None
        """
        self._query_string: str = query_str
        self._query_job_config: typing.Optional[bigquery.QueryJobConfig] = job_config
        
    def __new__(cls, query_str: str, job_config: typing.Optional[bigquery.QueryJobConfig] = None):
        """
        Internal method used to create the instance.

        Parameters
        ----------
        query_str : str
            Query string that will be used to query the BigQuery job.
        job_config: typing.Optional[bigquery.QueryJobConfig]
            QueryJobConfig type, used to configure the query parameters. By default None.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            Raised when the input query string fails validation.
        """
        if cls.validate_query(query_str):
            return super().__new__(cls)
        else:
            raise ValueError(f"Query has failed validation.")
        
    def add_job_config(self, **kwargs):
        """
        Method used to attach a QueryJobConfig instance to this object.

        Parameters
        ----------
        **kwargs
            Accepts named arguments corresponding to the kwargs used in the __init__ method of the QueryJobConfig object.

        Returns
        -------
        None

        Raises
        ------
        AttributeError
            Raised when attempting to set an unknown property.
        """
        try:
            self._query_job_config = bigquery.QueryJobConfig(**kwargs)
        except Exception as e:
            raise e
        
    def run_query(self, client: bigquery.Client) -> bool:
        """
        Method used to execute the query.
        
        Fails if the job configuration has not been setup.
        
        Parameters
        ----------
        client: bigquery.Client
            BigQuery client used to execute this query.

        Returns
        -------
        bool
            If query was successfully executed, returns True. Returns False otherwise.

        Raises
        ------
        ValueError
            Raised when job configuration has not been specified.
        """
        
        if self._query_job_config is None:
            error_msg: str = "Please specify a job configuration."
            raise ValueError(error_msg)

        query_job = client.query(
            self._query_string,
            job_config = self._query_job_config
        )
        
        job_errors: typing.Optional[typing.Mapping] = query_job.error_result
        
        if job_errors is not None:
            logging.error(f"Table was not updated due to the following error: {job_errors}")
            return False
        
        job_result = query_job.result()
        logging.info(f"Query was successful. Following records were added to the resource: {self._query_job_config.destination}")
        for row in job_result:
            logging.info(f"{row}")
        return True
        

def load_query(fp: str) -> BigQueryQuery:
    """
    Loading the query based on the given filepath.

    Parameters
    ----------
    fp : str
        Filepath pointing to the file containing the BigQuery Query string.

    Returns
    -------
    BigQueryQueryString
        Wrapper object representing the query string.

    Raises
    ------
    OSError
        Raised when there are issues with opening the file in the filepath.
    ValueError
        Raised when the fp fails validation checks.
    """
    
    # Validating the filepath
    # TODO: Add additional validation checks in the future.
    if len(fp) == 0:
        raise ValueError(f"Empty string passed as the filepath!")
    
    # Attempting to open the filepath
    with open(fp, "rt") as opened_file:
        raw_query_string: str = opened_file.read()
        
    # Constructing the BigQueryQueryString instance
    result = BigQueryQuery(raw_query_string)
    return result
    
        