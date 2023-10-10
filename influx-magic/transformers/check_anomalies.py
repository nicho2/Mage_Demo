import matplotlib.pyplot as plt

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    for uid in df.unique_id.unique():
        uid_df = df[df.unique_id == uid]
        if True in uid_df.is_anomaly.unique():

            anomalies = uid_df[uid_df.is_anomaly]
            # Create the plot
            fig, ax1 = plt.subplots()

            # Plot the first data set on the primary y-axis
            ax1.plot(uid_df.date, uid_df.score, label='Anomaly Score', color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')

            # Add the scatter point
            ax1.scatter(anomalies.date, anomalies.value, color='red', s=100, edgecolors='black', label='Anomaly')

            # Create a twin y-axis to plot the second data set
            ax2 = ax1.twinx()
            ax2.plot(uid_df.date, uid_df.value, label='Normalized Value', color='green')
            ax2.tick_params(axis='y', labelcolor='red')

            # Add title and labels
            plt.title(f'Anomalies - Power - {uid}')
            plt.xlabel('Value')
            plt.ylabel('Time')
            plt.legend()

            # Show the plot
            plt.show()


    return df

@test
def test_output(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert True not in df.is_anomaly.unique(), 'Anomalies exist 😱'