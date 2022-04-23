"""
Date: 22 Apr 2022

Author: Connor Keenum

Description:
    Geometric Brownian Motion is a special type of random motion, that may be applied to stock simulation.

Input:
    ticker = "ETH" : (Optional) String
    initial_date : Date
    end_date : Date
    mu : Float (Average value of returns)
    sigma : Float (Standard Deviation of returns)
    step = 1 : (Optional) Int (Number of seconds between each Query)

Output:


See also:
    https://www.analyticsvidhya.com/blog/2021/05/create-a-dummy-stock-market-using-geometric-brownian-motion-in-python/

"""
from datetime import datetime
import src.back_testing.conservative_momentum_backtest as bt
import random
import numpy as np
import matplotlib.pyplot as plt


def make_obj(ticker: str, date: datetime, value: float) -> dict:
    return {
        "ticker": ticker,
        "date": date,
        "value": value
    }

mu = 0.0010
sigma = .030
start_price = 2295

np.random.seed(0)
returns = np.random.normal(loc=mu, scale=sigma, size=365)
price = start_price*(1+returns).cumprod()

# print(price[40]) # Able to access price as if it were an array

mock_data = []
for x in range(1,len(price)):
    a = datetime.fromtimestamp(x*100000)
    b = float(price[x])
    mock_data.append(make_obj(ticker="ETH", date=a, value=b))

init_sma24 = random.uniform(261, 262)
init_sma12 = random.uniform(261, 263)

back_test = bt.conservative_momentum_backtest(mock_data, init_sma24, init_sma12, r=1.09, v=.95)
profitability = back_test[-1]["current_profitability_multiplier"]
print(f"Profitability: {profitability}")


plt.plot(price)
plt.show()