from slugify import slugify
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    df['unique_id'] = df.apply(lambda row: f"{slugify(row.provider)}-{row.machineID}", axis=1)

    df['ds'] = pd.to_datetime(df['time'], unit='us')
    # .astype(int)
    print(df.machineID.unique())
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
