from sklearn.preprocessing import MinMaxScaler
from darts import timeseries 
from darts.dataprocessing.transformers import Scaler

from forecasting.general_utilities.df_utils import *

class Dataset:

    def __init__(self, catchment_data) -> None:
        self.catchment_data = catchment_data
        self.scaler = Scaler(MinMaxScaler())
        self.target_scaler = Scaler(MinMaxScaler())


        current_dfs = self.catchment_data.all_current_data.copy()
        print("shape of current_dfs in Dataset init: ", current_dfs[0].shape)
        self.Xs_current, self.y_current = self._pre_process(current_dfs, fit_scalers=False)



        historical_dfs = self.catchment_data.all_historical_data.copy()
        self.Xs_historical, self.y_historical = self._pre_process(historical_dfs)

        self.X_trains, self.X_tests, self.X_validations, self.y_train, self.y_test, self.y_validation = self._partition()
  
        
    @property
    def num_X_sets(self):
        return len(self.X_trains)

        
    def _pre_process(self, dfs, fit_scalers=True):
        """
        Fetch needed data and perform all standard preprocessing.
        """
        Xs = []
        y = None
        for df in dfs:
            X_cur, y_cur = split_X_y(df)
            X_cur = self.add_engineered_features(X_cur)
            X_cur = timeseries.TimeSeries.from_dataframe(X_cur)
            y_cur = timeseries.TimeSeries.from_dataframe(y_cur)
            if fit_scalers:
                self.scaler.fit(X_cur)
                self.target_scaler.fit(y_cur)
                fit_scalers = False # Only fit scalers once

            X_cur = self.scaler.transform(X_cur)
            Xs.append(X_cur)
            #assert(y == None or y == y_cur)
            y = y_cur

 
        
        y = self.target_scaler.transform(y)

        return Xs, y

    def _partition(self, test_size=0.2, validation_size=0.2):
        X_trains = []
        X_tests = []
        X_validations = []
        for X in self.Xs_historical:
            X_train, X_test = X.split_after(1-test_size)
            X_train, X_validation = X_train.split_after(1-validation_size)

            X_trains.append(X_train)
            X_tests.append(X_test)
            X_validations.append(X_validation)

        y_train, y_test = self.y_historical.split_after(1-test_size)
        y_train, y_validation = y_train.split_after(1-validation_size)

        return (X_trains, X_tests, X_validations, y_train, y_test, y_validation)
    
    def add_engineered_features(self, df):
        df['day_of_year'] = df.index.day_of_year

        df['snow_10d'] = df['snow_1h'].rolling(window=10 * 24).sum()
        # df['snow_30d'] = df['snow_1h'].rolling(window=30 * 24).sum()
        df['rain_10d'] = df['rain_1h'].rolling(window=10 * 24).sum()
        # df['rain_30d'] = df['rain_1h'].rolling(window=30 * 24).sum()

        df['temp_10d'] = df['temp'].rolling(window=10 * 24).mean()
        # df['temp_30d'] = df['temp'].rolling(window=30 * 24).mean()
        print(df.shape)
        df.dropna(inplace=True)
        print(df.shape)
        return df