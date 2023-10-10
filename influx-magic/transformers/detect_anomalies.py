from river import compose
from river import datasets
from river import metrics
from river import preprocessing
from river import metrics
from river import utils
from river import anomaly
import plotly.express as px
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    
    anomaly_dfs = pd.DataFrame(columns=["date", "score", "value", "is_anomaly", "unique_id"])

    for uid in df.unique_id.unique():
        print(uid)
        
        model = compose.Pipeline(
            anomaly.HalfSpaceTrees(
                n_trees=5, 
                height=2, 
                window_size=250, 
                seed=1)
        )

        anomaly_df = pd.DataFrame(columns=["date", "score", "value", "is_anomaly", "unique_id"])
        
        sliced_df = df[df.unique_id == uid]
        
        sliced_df['normalized_power'] = \
            (sliced_df.power - sliced_df.power.min() ) / (sliced_df.power.max() - sliced_df.power.min())
        
        for index, row in sliced_df.iterrows():
            ds = row['ds']
            x = row['normalized_power']

            features = {uid: x}

            model = model.learn_one(features)
            score = model.score_one(features)

            anomaly_df = pd.concat([anomaly_df, pd.DataFrame(
                [{'date': ds, 'score': float(score), 'value': x, 'is_anomaly': score > .8, 'unique_id': uid}])
                                ])

        anomaly_dfs = pd.concat([anomaly_dfs, anomaly_df])

    return anomaly_dfs