from datetime import datetime
import random
import src.back_testing.conservative_momentum_backtest as bt
from src.data_processing.backtest_mock_data_generator import mock_data_generator_uniform

"""
Date: 22 Apr 2022

Author: Connor Keenum

Description:
    This file simply simulates the conservative momentum strategy using various techniques.
"""


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

uniform_dist_test(start, end, ticker, lowest, highest, query, repeat_test)
