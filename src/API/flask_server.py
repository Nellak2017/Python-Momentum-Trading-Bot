"""
Date: 12 May 2022

Author: Connor Keenum

Description:
    Host a REST API that will give access to the Stock Trading Algorithms.

API Endpoints:

    NAME            TYPE    ROUTE               PAYLOAD

    BacktestedData  GET     /?={query string}   Returns JSON of Back-tested Stock Data based on the Query String

"""
from flask import Flask, request
from flask_cors import CORS  # Used for localhost
from datetime import timedelta, date
import re
import src.back_testing.conservative_momentum_backtest as cm
import src.data_processing.stock_data_API as sd

app = Flask(__name__)
CORS(app)


@app.route('/ConservativeMomentum')
def get_backtested_data() -> list:
    # Get input parameters based on query string
    ticker: str = request.args['ticker']  #
    interval: str = request.args['interval'].lower()  #
    period: str = request.args['period'].lower()  #
    upper_sell: str = request.args['upperSell']
    lower_sell: str = request.args['lowerSell']
    init_holding: str = request.args['initHolding']

    # Parse the query strings
    try:
        upperSellTarget = float(upper_sell)
    except ValueError:
        raise ValueError(f'{upperSellTarget} is not a float')
    try:
        lowerSellTarget = float(lower_sell)
    except ValueError:
        raise ValueError(f'{lowerSellTarget} is not a float')
    try:
        holding = bool(init_holding)
    except ValueError:
        raise ValueError(f'{holding} is not a boolean')

    days: int = int(re.sub("[^0-9]", "", period))  # Convert period to an integer
    if period == "1w":
        days *= 7
    elif period == "1m":
        days *= 30
    elif period == "3m":
        days *= 90
    elif period == "1y":
        days *= 365
    elif period == "5y":
        days *= 365 * 5
    elif period == "all":
        days *= 365 * 5  # @todo: Figure out how to find how many days old a company is on the market
    else:
        days = days

    API_Data = sd.get_stock_data_in_range(ticker=ticker, interval=interval, period=period)
    end = date.today() - timedelta(days=days)
    end = end.strftime("%Y:%m:%d %H:%M:%S")

    sma24 = sd.get_sma_data_point(ticker, end, 24)[f'sma{24}']
    sma12 = sd.get_sma_data_point(ticker, end, 12)[f'sma{12}']

    return {"data": cm.conservative_momentum_backtest(data_set=API_Data, init_SMA_12=sma12, init_SMA_24=sma24, r=upperSellTarget,
                                                      v=lowerSellTarget, initially_holding=holding)}


if __name__ == '__main__':
    app.run(debug=True)

'''
?ticker=ETH-USD&interval=1d&period=1y&upperSell=1.1&lowerSell=.95&initHolding=False&lowerIndicator=EMA-12&upperIndicator=EMA-24

(data_set: list, init_SMA_24: float, init_SMA_12: float,initially_holding: bool = False, r: float = 1.1, v: float = .95) -> list:
'''
