from abc import ABC, abstractmethod

from rlf.forecasting.data_fetching_utilities.coordinate import Coordinate
from rlf.forecasting.data_fetching_utilities.weather_provider.api.models import Response


class BaseAPIAdapter(ABC):
    """Abstract base class for APIAdapter objects"""

    @abstractmethod
    def get_historical(elf, coordinate: Coordinate, start_date: str, end_date: str, columns: list[str] = None) -> Response:
        """Make a GET request to the API for historical/archived data.

        Args:
            coordinate (Coordinate): The location to fetch data for.
            start_date (str): The starting date for the requested data. In the format "YYYY-MM-DD".
            end_date (str): The ending date for the requested data. In the format "YYYY-MM-DD".
            columns (list[str], optional): The subset of columns to fetch. If set to None, all columns will be fetched. Defaults to None.

        Returns:
            Response: The response payload for the request
        """
        return NotImplementedError

    @abstractmethod
    def get_current(self, coordinate: Coordinate, past_days: int = 92, forecast_days: int = 16, columns: list[str] = None) -> Response:
        """Make a GET request to the API for current/forecasted data.

        Args:
            coordinate (Coordinate): The location to fetch data for.
            past_days (int, optional): How many days into the past to fetch data for. Defaults to 92 (OpenMeteo max value).
            forecast_days (int, optional): How many days into the future to fetch data for. Defaults to 16 (OpenMeteo max value).
            columns (list[str], optional): The subset of columns to fetch. If set to None, all columns will be fetched. Defaults to None.

        Returns:
            Response: The response payload for the request
        """
        return NotImplementedError
