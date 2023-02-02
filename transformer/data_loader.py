import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
import os
import torch
import numpy as np

from joblib import dump


# Anpassungen zur Vorarbeit vorgenommen
class SensorDataset(Dataset):

    def __init__(self, csv_name, root_dir, training_length, forecast_window):
        # load raw data file
        csv_file = os.path.join(root_dir, csv_name)
        self.df = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = MinMaxScaler()
        self.T = training_length
        self.S = forecast_window

    def __len__(self):
        # return number of sensors
        return len(self.df.groupby(by=["reindexed_id"]))

    def __getitem__(self, idx):
        idx = idx + 1
        start = np.random.randint(0, len(self.df[self.df["reindexed_id"] == idx]) - self.T - self.S)
        sensor_number = str(self.df[self.df["reindexed_id"] == idx][["sensor_id"]][start:start + 1].values.item())
        index_in = torch.tensor([i for i in range(start, start + self.T)])
        index_tar = torch.tensor([i for i in range(start + self.T, start + self.T + self.S)])
        _input = torch.tensor(self.df[self.df["reindexed_id"] == idx][
                                  ["values", "sin_hour", "cos_hour", "sin_day", "cos_day", "sin_month", "cos_month"]][
                              start: start + self.T].values)
        target = torch.tensor(self.df[self.df["reindexed_id"] == idx][
                                  ["values", "sin_hour", "cos_hour", "sin_day", "cos_day", "sin_month", "cos_month"]][
                              start + self.T: start + self.T + self.S].values)

        scaler = self.transform

        scaler.fit(_input[:, 0].unsqueeze(-1))
        _input[:, 0] = torch.tensor(scaler.transform(_input[:, 0].unsqueeze(-1)).squeeze(-1))
        target[:, 0] = torch.tensor(scaler.transform(target[:, 0].unsqueeze(-1)).squeeze(-1))

        dump(scaler, 'scalar_item.joblib')

        return index_in, index_tar, _input, target, sensor_number
