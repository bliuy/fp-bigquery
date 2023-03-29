from google.cloud import bigquery


SQL_QUERY: str = r"""
select port_name, distance_in_meters
from (
  select *, rank() over (order by t1.distance_in_meters asc) ranked
  from (
    select remainingPorts.port_Name port_name,ST_DISTANCE(sgPort.port_geom, remainingPorts.port_geom) distance_in_meters
    from `takehomeassignment-382012.bigqueryassignment.world_port_index` sgPort
    cross join `takehomeassignment-382012.bigqueryassignment.world_port_index` remainingPorts
    where sgPort.port_name = 'JURONG ISLAND' and sgPort.country = 'SG' and remainingPorts.port_name != 'JURONG ISLAND'
  ) t1
) t2
where ranked <= 5
"""

TABLE_ID: str = "takehomeassignment-382012.bigqueryassignment.Q1"
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(
    destination = TABLE_ID
)

query_job = client.query(SQL_QUERY, job_config=job_config)
job_results = query_job.result()
for result in job_results:
    print(f"Job result: {result}")


