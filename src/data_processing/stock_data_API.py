import yfinance as yf
from datetime import datetime, timedelta
from pytz import timezone

# See also: https://medium.com/analytics-vidhya/python-how-to-get-bitcoin-data-in-real-time-less-than-1-second-lag-3877
# 2da43740
# see also: https://towardsdatascience.com/the-easiest-way-to-pull-stock-data-into-your-python-program-yfinance-
# 82c304ae35dc

"""
Date: 7 May 2022

Author: Connor Keenum

Description:
    This file allows you to get Real Life Stock data using yfinance library API.

Libraries Needed:
    yfinance
    datetime
"""


def get_stock_data_in_range(ticker: str, interval: str, start: str = None, end: str = None, period: str = None) -> list:
    """
    :param ticker: Stock Ticker.
    :param interval: The Query Period for the stock. 1m,2m,5m,15m,30m,90m,1h,1d,5d,1wk,1mo,3mo
    :param start: The Start period for which to consider the stock. String format is yyyy-mm-dd.
    :param end: The End period for which to consider the stock.  String format is yyyy-mm-dd.
    :param period: The Time Period for which to consider the stock. 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    :return: A list of dictionaries of stock market data, readable by the Back Testers.
    """
    if interval not in ["1m", "2m", "5m", "15m", "30m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]:
        raise ValueError('The "get_stock_data_in_range" received an invalid interval parameter.')
    if period not in ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max", None]:
        raise ValueError('The "get_stock_data_in_range" received an invalid period parameter.')
    data = yf.download(tickers=ticker, interval=interval, start=start, end=end, period=period)

    li = data.to_dict('index')
    ld = data[['Open']].to_dict('records')
    retData = []
    count = 0
    for x in li.keys():
        ld[count]['ticker'] = ticker
        ld[count]['date'] = x.to_pydatetime().astimezone(timezone('America/Chicago')).strftime("%Y:%m:%d %H:%M:%S")
        ld[count]['value'] = ld[count]['Open']
        del ld[count]['Open']
        retData.append(ld[count])
        count += 1

    return retData


'''
d = get_stock_data_in_range(ticker="ETH-USD", interval="1h", period="1d")
for x in d:
    print(x)
'''


def get_stock_data_point(ticker: str) -> dict:
    """
    :param ticker: Stock Ticker.
    :return: A dictionary of the Stock values.
    """
    stock_info = yf.Ticker(ticker=ticker).info
    market_price = stock_info['regularMarketPrice']
    now = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    data_point = {
        "ticker": ticker,
        "date": now,
        "value": market_price
    }
    return data_point


def get_sma_data_point(ticker: str, date: str, days: float) -> dict:
    """
    :param ticker: Stock Ticker.
    :param date: Date querying SMA.
    :param days: SMA_days(day). Example: SMA_50("ETH-USD", "2022:05:04 00:00:00")
    :return: A dictionary of the SMA value.
    """
    end = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
    start = end - timedelta(days=days)
    data = yf.download(tickers=ticker, start=start, end=end, period="1d")
    data[f"sma{days}"] = data['Adj Close'].rolling(days).mean()
    return {"ticker": ticker, "date": date, f"sma{days}": data.iloc[-1][f'sma{days}']}

#print(get_sma_data_point("ETH-USD", "2021:05:13 00:00:00", 24))

def get_ema_data_point(ticker: str, date: str, days: float) -> dict:
    """
    :param ticker: Stock Ticker.
    :param date: Date querying EMA.
    :param days: EMA_days(day). Example: EMA_50("ETH-USD", "2022-05-04 00:00:00+00:00")
    :return: A dictionary of the EMA value.
    """
    pass

# print(get_stock_data_point("ETH-USD"))
