from datetime import datetime
import random
import src.back_testing.conservative_momentum_backtest as bt
from src.data_processing.backtest_mock_data_generator import mock_data_generator_uniform

"""
Date: 22 Apr 2022

Author: Connor Keenum

Description:
    This file simply simulates the conservative momentum strategy using various techniques, many hundreds of times.
    The only display for this is the Console. If you want to visualize it, go to the other simulation for this.
"""


# @ todo: Make the simulator for Geometric Brownian Motion
def uniform_dist_test(start, end, ticker, lowest, highest, query, repeat_test):
    init_date = datetime.fromtimestamp(start)
    end_date = datetime.fromtimestamp(end)
    init_sma24 = random.uniform(lowest, highest)
    init_sma12 = random.uniform(lowest, highest)
    sum_ = 0

    print("")
    print(f"Testing each Trading Strategy {repeat_test} times")
    print("-" * 30)
    for test in range(repeat_test):
        mock_data = mock_data_generator_uniform(ticker, init_date, end_date, lowest, highest, query)
        back_test = bt.conservative_momentum_backtest(mock_data, init_sma24, init_sma12)

        if test % (repeat_test//10) == 0 or test == repeat_test-1:
            pass
            # print("#",end="")
            # print(f"{int((test / repeat_test)*100)}%")

        profitability = back_test[-1]["current_profitability_multiplier"]
        sum_ += profitability

    print("")
    print("-" * 30)
    print(f"Average profitability: {sum_/repeat_test}")


start = 1_572_014_192
end = start + 10
ticker = "ETH"
lowest = 2000
highest = 3500
query = 1  # query every second
repeat_test = 100000
init_date = datetime.fromtimestamp(start)
end_date = datetime.fromtimestamp(end)
'''
uniform_dist_test(start, end, ticker, lowest, highest, query, repeat_test)

'''
mock_data = [
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start), 'value': 3},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+1*86400), 'value': 2},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+2*86400), 'value': 3.33},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+3*86400), 'value': 2.75},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+4*86400), 'value': 2.6},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+5*86400), 'value': 3.05},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+6*86400), 'value': 2.9},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+7*86400), 'value': 3.04},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+8*86400), 'value': 2.71},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+9*86400), 'value': 2.45},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+10*86400), 'value': 2.24},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+11*86400), 'value': 2.26},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+12*86400), 'value': 2.55},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+13*86400), 'value': 2.8},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+14*86400), 'value': 3.01},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+15*86400), 'value': 3.05},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+16*86400), 'value': 3.2},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+17*86400), 'value': 3.25},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+18*86400), 'value': 3.48},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+19*86400), 'value': 3.54},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+19*86400), 'value': 3.54},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+19*86400), 'value': 3.64},
    {'ticker': 'WORK', 'date': datetime.fromtimestamp(start+19*86400), 'value': 3.74},
    ]
sma24 = 3
sma12 = 3

backtest = bt.conservative_momentum_backtest(mock_data, sma24, sma12)

for x in backtest:
    print(x)