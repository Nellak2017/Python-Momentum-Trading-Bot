import yahoo_fin
from yahoo_fin import stock_info
import datetime

"""
Date: 23 Apr 2022

Author: Connor Keenum

Description:
    This file allows you to get Real Life Stock data using yahoo_fin library API.

Libraries Needed:
    yahoo_fin
    datetime
"""


# @ todo: Learn how to deal with Data frame objects from Pandas for the API
def get_stock_data_in_range() -> list:
    pass


# @ todo: Unit test this with mock API
# @ todo: Verify that the SMA is accurate for any given interval. For the default interval it seems to work (citation?)
def get_sma(ticker: str, days: int, interval: str, start: datetime = None, end: datetime = None) -> float:
    """
    :param start: The Start period for which to consider the SMA. -50 means 50 days ago.
    :param end: The End period for which to consider the SMA. 0 means today.
    :param interval: The Query Period for the stock. Example: 1d, 1w, 1m
    :param ticker: Stock Ticker.
    :param days: Number of days to consider the Simple Moving Average.
    """
    # Will be a Pandas Data frame converted into a float
    return yahoo_fin.stock_info.get_data(ticker, start_date=start, end_date=end,
                                         interval=interval)['close'][-days:].mean()


start = datetime.date(2021, 4, 26)
end = datetime.date(2021, 6, 16)
#print(get_sma("AAPL", 50, "1d", start=start, end=end))
#print(yahoo_fin.stock_info.get_stats("nflx"))

def get_stock_data_point() -> dict:
    pass
