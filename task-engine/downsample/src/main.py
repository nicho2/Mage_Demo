from flightsql import FlightSQLClient
from os import getenv
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from time import sleep




# IOX
host = getenv("INFLUX_HOST", "eu-central-1-1.aws.cloud2.influxdata.com")
org = getenv("INFLUX_ORG", "6a841c0c08328fb1")
bucket = getenv("INFLUX_BUCKET", "traces")
token = getenv("INFLUX_TOKEN", "foo")
interval = getenv("INTERVAL", 300)

client = FlightSQLClient(host=host,
                        token=token,
                        metadata={'bucket-name': bucket},
                        features={'metadata-reflection': 'true'})

influxdb_client = InfluxDBClient(url=("https://"+str(host)), token= token, org=org)
influxdb_write_api = influxdb_client.write_api(write_options=SYNCHRONOUS, batch_size=20, flush_interval=20, max_retries=0)

query = '''
SELECT
  DATE_BIN(INTERVAL '1 MINUTE', time, '1970-01-01T00:00:00Z'::TIMESTAMP) AS time,
  "machineID",
  avg(temperature) AS 'avg_temp',
  avg(load) AS 'avg_load',
  avg(vibration) AS 'avg_vibration',
  avg(power) AS 'avg_power'
FROM "machine_data" WHERE time > (NOW() - INTERVAL '5 MINUTE')
GROUP BY 2, 1
ORDER BY 2 , 1 desc
'''

while True:

    # Execute a query against InfluxDB's Flight SQL endpoint                        
    query = client.execute(query)
    
    # Create reader to consume result
    reader = client.do_get(query.endpoints[0].ticket)
    
    # Read all data into a pyarrow.Table
    Table = reader.read_all()
    print(Table, flush=True)
    
    # Parse the table and write to InfluxDB
    print("Downsampling data...", flush=True)
    #df = Table.to_pandas()
    #print(df, flush=True)
    #df = df.set_index('time')
    df = pl.from_arrow(Table)
    print(df, flush=True)


    # Write to InfluxDB
    print("Writing data to InfluxDB...", flush=True)
    influxdb_write_api.write(bucket=bucket, record=df, data_frame_measurement_name='machine_data_aggregated', data_frame_tag_columns=['machineID'])
    print(f"Sleeping for {interval} ", flush=True)
    sleep(int(interval))


        


