from datetime import datetime
import random
import numpy as np

import matplotlib.pyplot as plt
import src.back_testing.conservative_momentum_backtest as bt
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
    step = 1 : (Optional) Int (Number of seconds between each Query)

Output: (Will be displayed using strategy_display)
    data_points : [dict] (All the position data. They have fields "ticker", "date", and "value")

Libraries Needed:
    Date parsing
    Random Number Generator
    Numpy
"""


# Support Methods
# -----------------
def make_obj(ticker: str, date: datetime, value: float) -> dict:
    return {
        "ticker": ticker,
        "date": date,
        "value": value
    }


def brownian(mu: float = .001, sigma: float = .001, start_price: float = 1000, size: int = 365, seed: int = 0) -> list:
    """
    :param mu: Drift factor. Larger number indicates more bullish trend.
    :param sigma: Volatility factor. Larger number indicates more volatile.
    :param start_price: Initial Price on random walk.
    :param size: Number of days you want to simulate.
    :param seed: RNG seed value.
    :return: A list of prices.
    """
    np.random.seed(seed)
    returns = np.random.normal(loc=mu, scale=sigma, size=size)
    price = start_price * (1 + returns).cumprod()
    return list(price)


# -----------------
# Data Generators

def mock_data_generator_uniform(ticker: str, initial_date: datetime, end_date: datetime, low_value: float,
                                high_value: float, step: int = 1) -> list:
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


def mock_data_generator_geometric_brownian(ticker: str, initial_date: datetime, end_date: datetime, start_price: float,
                                           step: int = 1, mu: float = 0.0012, sigma: float = .032,
                                           seed: int = 0) -> list:
    """
    :param seed: RNG seed value.
    :param sigma: Volatility factor. Larger number indicates more volatile.
    :param mu: Drift factor. Larger number indicates more bullish trend.
    :param ticker: The Stock Ticker
    :param initial_date: The Initial Date of mock_data generation
    :param end_date: The End Date of mock_data generation
    :param start_price: The Lowest value that will be in the mock data generator
    :param step: How often you will query the Fake API, measured in seconds
    :return: Returns a List of Dictionaries that contain the stock data at each point
    """
    data_points: list = []
    start_date_as_int: int = int(datetime.timestamp(initial_date))
    end_date_as_int: int = int(datetime.timestamp(end_date))

    brownian_data_points: list = brownian(mu=mu, sigma=sigma, start_price=start_price,
                                          size=(end_date_as_int-start_date_as_int), seed=seed)

    index: int = 0
    for unix_time in range(start_date_as_int, end_date_as_int, step):
        mock_date: datetime = datetime.fromtimestamp(unix_time).strftime("%d-%b-%Y (%H:%M:%S.%f)")
        mock_value: float = brownian_data_points[index]
        data_points.append(make_obj(ticker, mock_date, mock_value))
        index += 1

    return data_points

# Simple test to see if it runs properly

start = 1_572_014_192
end = start + 365
sdate = datetime.fromtimestamp(start)
edate = datetime.fromtimestamp(end)
ticker = "ETH"
lowest = 2000
query = 1  # query every second
repeat_test = 2000
begin_test = 500
init_sma24 = 2000
init_sma12 = 2030

sum_ = 0
for seed in range(begin_test, begin_test+repeat_test):
    data_pts = mock_data_generator_geometric_brownian(ticker=ticker, initial_date=sdate, end_date=edate,
                                                      start_price=lowest, seed=seed, mu = 0.0015)
    back_test = bt.conservative_momentum_backtest(data_pts, init_sma24, init_sma12, r=1.10, v=.95)
    profitability = back_test[-1]["current_profitability_multiplier"]
    sum_ += profitability

'''
price = []
for data in data_pts:
    price.append(data["value"])

'''

print(f"Average Profitability for {repeat_test-begin_test} trials = {sum_ / repeat_test}")
print(f"5-year profitability, {sum_ / repeat_test}^5 = {(sum_ / repeat_test)**5}")


'''
plt.plot(price)
plt.show()

'''









