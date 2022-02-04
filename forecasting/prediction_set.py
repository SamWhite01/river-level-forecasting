from pandas import DataFrame
from datetime import timedelta

from forecasting.data_fetching_utilities.weather import *
from forecasting.data_fetching_utilities.level import *
from forecasting.general_utilities.df_utils import *

class PredictionSet:

    def __init__(self, data_fetcher, dataset) -> None:
        """
        Produce a processed inference set for the given forecast site. Adheres to given shape/scaler.
        Args:
            data_fetcher (DataFetcher): Forecast site from which data should be fetched.
            X_shape (tuple): input shape for target model.
            scaler (MinMaxScaler): Scaler used on model training data.
        """
        self.data_fetcher = data_fetcher
        self.X_shape = dataset.input_shape
        self.scaler = dataset.scaler
        self.target_scaler = dataset.target_scaler

        self.X, self.y = self._pre_process()
        

    def _pre_process(self):
        """
        Fetch needed data and perform all standard preprocessing.
        Returns:
            df (DataFrame): Processed dataframe.
        """
        df = self.data_fetcher.all_current_data.copy()
        df = add_lag(df)
        X, y = split_X_y(df)
        X = scale(X, self.scaler, fit_scalers=False)
        y = scale(y, self.target_scaler, fit_scalers=False)

        return X,y


    def x_in_for_window(self, start, window_size_hours=5) -> DataFrame:
        """
        Grab an isolated dataframe for the given window.
        Args:
            start (datetime): Start of window.
            window_size_hours (int, optional): Duration of window in hours. Defaults to 5.
        Returns:
            x_in (np.array): dataset trimmed down to the given window. Reshaped according to self.X_shape.
        """
        # Typechecks and guard clauses to increase callsite flexibility TODO: minimize need upstream
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        end = start + timedelta(hours=window_size_hours-1)
        if start not in self.df.index:
            print("ERROR: invalid start timestamp")
            return None
        if end not in self.df.index:
            print("ERROR: invalid end timestamp")
            return None
        print(start)
        print(end)
        x_in = self.df.loc[start:end, :]
        print(x_in)
        print(x_in.shape)
        print(self.X_shape)
        x_in = x_in.values.reshape(self.X_shape)
        return x_in
    
    def update(self):
        """
        Force an update for forecast site data, re-fetch and re-process. Call hourly at minimum when forecasting.
        """
        self.data_fetcher.update_for_inference()
        self.df = self._pre_process()