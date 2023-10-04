if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(data, *args, **kwargs):
    if True in data.is_anomaly.unique():
        raise ValueError("There's an anomaly!")
    else:
        return data




