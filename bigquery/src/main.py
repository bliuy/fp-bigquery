import logging
import typing

# Setting logger level
logging.root.setLevel(logging.INFO)

try:
    from google.cloud import bigquery
    import google.auth.exceptions as g_exceptions
    from functions import helper_functions as fn
except ImportError as e:
    logging.error(f"Failed to import the Google Cloud Python API. Please ensure that it's installed.")
    raise e



def main():    
    # Constants
    JobInformation = typing.NamedTuple("JobInformation", [("table_id", str), ("sql_filepath", str)])
    context: typing.Dict[int, JobInformation] = {}
    context[1] = JobInformation(r"takehomeassignment-382012.bigqueryassignment.Q1", r"src/queries/bq-1.txt")
    context[2] = JobInformation(r"takehomeassignment-382012.bigqueryassignment.Q2", r"src/queries/bq-2.txt")
    context[3] = JobInformation(r"takehomeassignment-382012.bigqueryassignment.Q3", r"src/queries/bq-3.txt")

    # Creating the client
    try:
        client = bigquery.Client()
    except g_exceptions.DefaultCredentialsError as e:
        logging.error(f"Unable to authenticate with the default credentials. Please check that the environment vars have been correctly set.")
        return None
    
    # Creating job configurations
    jobs: typing.Dict[int, fn.BigQueryQuery] = {}
    for k,v in context.items():
        tbl_id, fp = v
        job = fn.load_query(fp)
        job.add_job_config(destination=tbl_id)
        jobs[k] = job
    
    # Executing the various jobs
    for i, job in jobs.items():
        logging.info(f"Executing Job #{i} now.")
        try:
            job.run_query(client=client)
        except Exception as e:
            logging.error(f"Job #{i} has failed!")
    
if __name__ == "__main__":
    main()

