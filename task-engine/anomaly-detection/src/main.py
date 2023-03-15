from flightsql import FlightSQLClient
from os import getenv
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from time import sleep
from adtk.data import validate_series
from adtk.detector import LevelShiftAD



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

query = client.execute("SELECT \"machineID\" FROM iox.machine_data WHERE time > (NOW() - INTERVAL '15 MINUTE')")
# Create reader to consume result
reader = client.do_get(query.endpoints[0].ticket)

# Read all data into a pyarrow.Table
Table = reader.read_all()
print(Table)

d = Table.to_pydict()
machines = d['machineID']



while True:

   for machine in machines:
      query = client.execute(f"SELECT \"machineID\", vibration, time FROM iox.machine_data WHERE time > (NOW() - INTERVAL '5 MINUTE') AND \"machineID\" = '{machine}'")
      # Create reader to consume result
      reader = client.do_get(query.endpoints[0].ticket)

      # Read all data into a pyarrow.Table
      Table = reader.read_all()
      print(Table)
            # Convert to Pandas DataFrame
      df = Table.to_pandas().set_index("time")
      df_temp = df.drop(columns=["machineID"])

      s_train = validate_series(df_temp)
      level_shift_ad = LevelShiftAD(c=6.0, side='both', window=5)
      anomalies = level_shift_ad.fit_detect(s_train, return_list=False).rename(columns={"vibration": "anomalies"})


      df = df.merge(anomalies, on="time", how="left")
      df["anomalies"] = df["anomalies"].fillna(0).astype(int)
      print(df)

      # Write to InfluxDB
      print("Writing data to InfluxDB...", flush=True)
      influxdb_write_api.write(bucket=bucket, record=df, data_frame_measurement_name='machine_data_aggregated', data_frame_tag_columns=['machineID'])
      print(f"Sleeping for {interval} ", flush=True)
      sleep(int(interval))


        


