from datetime import datetime
import random
"""
Date: 22 Apr 2022

Author: Connor Keenum

Description:
    For this data generator, we're going to generate mock data for testing the back testers.

Input:
    ticker : String
    initial_date : Date
    end_date : Date
    low_value : Float (Lowest randomly generated value)
    high_value : Float (Highest randomly generated value)
    step = 3600 : (Optional) Int (Number of seconds between each Query)

Output: (Will be displayed using strategy_display)
    data_points : [dict] (All the position data. They have fields "ticker", "date", and "value")

Libraries Needed:
    Date parsing
    Random Number Generator
"""


def make_obj(ticker: str, date: datetime, value: float) -> dict:
    return {
        "ticker": ticker,
        "date": date,
        "value": value
    }


def mock_data_generator(ticker: str, initial_date: datetime, end_date: datetime, low_value: float,
                        high_value: float, step: int) -> list:
    """
    :param ticker: The Stock Ticker
    :param initial_date: The Initial Date of mock_data generation
    :param end_date: The End Date of mock_data generation
    :param low_value: The Lowest value that will be in the mock data generator
    :param high_value: The Highest value that will be in the mock data generator
    :param step: How often you will query the Fake API, measured in seconds
    :return: Returns a List of Dictionaries that contain the stock data at each point
    """
    data_points: list = []
    start_date_as_int: int = int(datetime.timestamp(initial_date))
    end_date_as_int: int = int(datetime.timestamp(end_date))

    for unix_time in range(start_date_as_int, end_date_as_int, step):
        mock_date: datetime = datetime.fromtimestamp(unix_time).strftime("%d-%b-%Y (%H:%M:%S.%f)")
        mock_value: float = random.uniform(low_value, high_value)
        data_points.append(make_obj(ticker, mock_date, mock_value))

    return data_points
