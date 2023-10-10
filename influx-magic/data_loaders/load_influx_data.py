from influxdb_client_3 import InfluxDBClient3
import os
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    client = InfluxDBClient3(
        host=os.getenv('INFLUX_HOST'),
        token=os.getenv('INFLUX_TOKEN'),
        database=os.getenv('INFLUX_DATABASE')
    )

    table = client.query(
        query="SELECT * FROM machine_data",
        language="sql"
        )

    client.close()

    df = table.to_pandas()
    
    time_data = df['time'].values.astype('datetime64[us]')
    
    df['time'] = pd.to_datetime(time_data)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
