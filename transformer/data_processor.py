import logging
import random

import pandas as pd
import numpy as np
import datetime


# Vollständig selbst geschrieben (Vorlage aus Tutorial)
def processData(filename):
    try:
        df = pd.read_csv(filename, index_col=0)
        timestamps = []
        for ts in df['timestamp']:
            date = ts.split("T")[0]
            time = ts.split("T")[1]
            entry = str(date) + " " + str(time)
            timestamps.append(entry)

        timestamps_hour = np.array(
            [float(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').hour) for t in timestamps])
        timestamps_day = np.array(
            [float(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').day) for t in timestamps])
        timestamps_month = np.array(
            [float(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').month) for t in timestamps])

        hours_in_day = 24
        days_in_month = 30
        month_in_year = 12
        new_df = pd.DataFrame()

        new_df['sensor_id'] = df['sensor_id']
        new_df['timestamps'] = timestamps
        new_df['values'] = df['VALUE_X_CURRENT']
        new_df['reindexed_id'] = None
        new_df['sin_hour'] = np.sin(2 * np.pi * timestamps_hour / hours_in_day)
        new_df['cos_hour'] = np.cos(2 * np.pi * timestamps_hour / hours_in_day)
        new_df['sin_day'] = np.sin(2 * np.pi * timestamps_day / days_in_month)
        new_df['cos_day'] = np.cos(2 * np.pi * timestamps_day / days_in_month)
        new_df['sin_month'] = np.sin(2 * np.pi * timestamps_month / month_in_year)
        new_df['cos_month'] = np.cos(2 * np.pi * timestamps_month / month_in_year)
        value = random.randrange(1, 44, 5)
        new_df = new_df.assign(reindexed_id=1)
        new_df = new_df.assign(sensor_id=str(value))
        return new_df


    except Exception as e:
        logging.error("Failed to transform the data into a matching format. Error-Log: " + str(e))


def SelectData():
    test = processData("./source/task_test.csv")

    test.to_csv(r'./source/test_dataset.csv', index=False)

    train = processData("./source/task_train.csv")
    train.to_csv(r'./source/train_dataset.csv', index=False)


if __name__ == "__main__":
    SelectData()
