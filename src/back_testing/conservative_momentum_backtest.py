import src.strategies.indicators.ema as ema
import src.strategies.evaluation_functions.momentum_strategy_evaluation as mse
import src.data_processing.stock_data_API as sd

"""
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    "Momentum investing" means investing in the stocks that have increased in price the most.
    For this back_testing, we're going to analyze a given stock and output the profitability data of the strategy.

Strategy:
    Sell at +10% or -5%, if -5% sell then wait until momentum indicator
    to buy. We will use momentum_strategy_evaluation to determine when to buy/sell/hold at any point.

Input:
    Data : [dict]
    Initially_Holding = False : (Optional) Boolean
    init_SMA_24 : Float 
    init_SMA_12 : Float
    r : Float (Upper Target Sell)
    v : Float (Lower Target Sell)

Output: (Will be displayed using strategy_display or in a console simulation)
    store : [Map] (All the positions meta-data after everything is over. Last element has profitability)
"""


# @todo: unit test this function
# @todo: add date object parsing
# @todo: query API for initial SMA values
# @todo: query API for data_set
# @todo: create mock_data generator for this function so that it may be easily unit tested
# @todo: Address the Edge Case where SMA12 and SMA24 initially are equal, it leads to a None Evaluation which is wrong
# @todo: Address the Error where profitability is updated when bought for certain cases
# noinspection PyUnusedLocal
def conservative_momentum_backtest(data_set: list, init_SMA_24: float, init_SMA_12: float,
                                   initially_holding: bool = False, r: float = 1.1, v: float = .95) -> list:
    """
    :param r: Upper Target Sell
    :param v: Lower Target Sell
    :param data_set: List of Dicts that is our Stock Data possibly from an API
    :param init_SMA_24: Simple Moving Average 24
    :param init_SMA_12: Simple Moving Average 12
    :param initially_holding: Whether you have the stock or not, initially false
    :return: list of dicts containing all the stock meta-data
    """

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    BH = "BUY and HOLD"
    SH = "SELL and HOLD"
    SB = "SELL and BUY"
    HH = "HOLD and HOLD"
    position_two_step_evaluation: str = HH
    next_position_evaluation: str = HOLD        # Next Evaluation, used for 2 step evaluation
    position_evaluation: str = HOLD             # Initial Evaluation defaults to HOLD
    store: list = []                            # Holds all the Meta-data for each position, stored for display purposes
    buy_point: float = data_set[1]["value"]     # The value that you bought a stock at
    sell_point: float = data_set[1]["value"]    # The value that you sold a stock at
    profitability_multiplier: float = 1.0       # Updated iteratively starting at 1
    holding: bool = initially_holding           # Changes based off evaluation function
    EMA_24_1: float = init_SMA_24               # Has to start as init_SMA_24
    EMA_12_1: float = init_SMA_12               # Has to start as init_SMA_12

    for data_index in range(len(data_set) - 3):
        # get value_1 and value_2 from data_set
        value_1 = data_set[data_index]["value"]
        value_2 = data_set[data_index + 1]["value"]
        value_3 = data_set[data_index + 2]["value"]
        value_4 = data_set[data_index + 3]["value"]

        # calculate indicators using provided indicator function
        EMA_24_2 = ema.ema(prev_ema=EMA_24_1, data_point=value_1, days=24)
        EMA_12_2 = ema.ema(prev_ema=EMA_12_1, data_point=value_1, days=12)

        # compose eval_dto using indicators
        eval_dto = {
            "value_1": value_1,
            "value_2": value_2,
            "ema24_1": EMA_24_1,
            "ema24_2": EMA_24_2,
            "ema12_1": EMA_12_1,
            "ema12_2": EMA_12_2,
            "stock_holding": holding,
            "buy_point": buy_point
        }

        # evaluate this position, passing in dto and store data
        position_evaluation = mse.evaluate_position(data_point=eval_dto, r=r, v=v)
        if position_evaluation not in [BUY, SELL, HOLD]:
            raise ValueError('The Evaluation Function Returned an unexpected value.')

        EMA_24_1 = EMA_24_2                     # Updated with New Previous Ema values
        EMA_12_1 = EMA_12_2                     # Updated with New Previous Ema values
        EMA_24_2 = ema.ema(prev_ema=EMA_24_2, data_point=value_1, days=24)
        EMA_12_2 = ema.ema(prev_ema=EMA_12_2, data_point=value_1, days=12)

        # update related variables for the store
        if position_evaluation == BUY:
            # next_position_evaluation = BUY
            buy_point = value_2
            #profitability_multiplier *= (sell_point / buy_point)
            holding = True
        elif position_evaluation == SELL:
            # next_position_evaluation = SELL
            sell_point = value_2
            profitability_multiplier *= (sell_point / buy_point)
            holding = False
        else:
            pass
            #next_position_evaluation = HOLD

        eval_dto_next = {
            "value_1": value_3,
            "value_2": value_4,
            "ema24_1": EMA_24_1,
            "ema24_2": EMA_24_2,
            "ema12_1": EMA_12_1,
            "ema12_2": EMA_12_2,
            "stock_holding": holding,
            "buy_point": buy_point
        }
        next_position_evaluation = mse.evaluate_position(data_point=eval_dto_next, r=r, v=v)
        if next_position_evaluation not in [BUY, SELL, HOLD]:
            raise ValueError('The "Next" Evaluation Function Returned an unexpected value.')

        if position_evaluation == BUY:
            position_two_step_evaluation = BH
        elif position_evaluation == SELL and next_position_evaluation == HOLD:
            position_two_step_evaluation = SH
        elif position_evaluation == SELL and next_position_evaluation == BUY:
            position_two_step_evaluation = SB
        else:
            position_two_step_evaluation = HH

        # update store
        store.append({
            "ticker": data_set[data_index]["ticker"],
            "date": data_set[data_index]["date"],
            "value": value_2,
            "ema24": EMA_24_1,
            "ema12": EMA_12_1,
            "holding_stock": holding,
            "current_profitability_multiplier": profitability_multiplier,
            "position_evaluation": position_evaluation,
            "position_two_step_evaluation": position_two_step_evaluation
        })

    return store


'''
mock_data_set = [
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 2000
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 2001
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 2002
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 2003
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1970
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1955
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1960
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1950
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1970
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1920
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1930
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1910
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1905
    },
    {
        "ticker": "ETH",
        "date": "Today at noon",
        "value": 1890
    },
]
sma24 = 1999
sma12 = 2004

results = conservative_momentum_backtest(data_set=mock_data_set, init_SMA_24=sma24, init_SMA_12=sma12)

for data_point in results:
    print(data_point)

'''
API_Data = sd.get_stock_data_in_range(ticker="ETH-USD", interval="1d", period="1y")

''' 
# ETH --> Default conservative strat 1y is .6795 (r=1.1,v=.95)
# ETH --> Best with conservative strat 1y is .91467 (r=1.3,v=.7)
# ETH --> Buy at start of year, sell at end is 3852.00 and 2634.93 == .68
sma24 = 2685.78
sma12 = 3029.18
'''

''' 
# MSFT --> Default conservative strat 1y is 1.0522 (r=1.10, v=.95)
# MSFT --> Best with conservative strat 1y is 1.10044 (r=1.18, v=.96)
# MSFT --> Buy at start of year, sell at end is 247.18 and 274.73 == 1.11
sma24 = 8594.95
sma12 = 8837.43
'''

'''
# DOGE --> Default conservative strat 1y is .5795 (r=1.10,v=.95)
# DOGE --> Best with conservative strat 1y is .892 (r=1.13,v=.955)
# DOGE --> Buy at start of year, sell at end is .6525 and .1275 == .1954
sma24 = .35
sma12 = .42
'''

'''
# SPXS --> Default conservative strat 1y is .974 (r=1.10,v=.95)
# SPXS --> Best with conservative strat 1y is 1.10431 (r=1.12,v=.92)
# SPXS --> Buy at start of year, sell at end is 26.47 and 22.34 == .84
sma24 = 27.35
sma12 = 26.73
'''

'''
# NIO --> Default conservative strat 1y is .817 (r=1.10,v=.95)
# NIO --> Best with conservative strat 1y is .8328 (r=1.25,v=.9)
# NIO --> Buy at start of year, sell at end is 34.33 and 14.92 == .434
sma24 = 38.28
sma12 = 39.01
'''

'''
# TSLA --> Default conservative strat 1y is .9197 (r=1.1,v=.95)
# TSLA --> Best conservative strat 1y is 1.13 (r=2,v=.8)
# TSLA --> Buy at start of year, sell at end is 617.2 and 873.28 == 1.414
sma24 = 702.16
sma12 = 687.3

'''

'''
# NVDA --> Default conservative strat 1y is 1.2795 (r=1.1,v=.95)
# NVDA --> Best conservative strat 1y is 1.5088 (r=1.4,v=.95)
# NVDA --> Buy at start of year, sell at end is 142.6575 and 186.75 == 1.309
sma24 = 150.33
sma12 = 149.15

'''

''' 2y
# AMD --> Default conservative strat 2y is 1.3212 (r=1.1,v=.95)
# AMD --> Best conservative strat 2y is 1.4079 (r=1.4,v=.95)
# AMD --> Buy at start of period, sell at end is 53.19 and 93.87 == 1.76
sma24 = 53.11
sma12 = 53.50

'''

sma24 = 2685.78
sma12 = 3029.18

results = conservative_momentum_backtest(data_set=API_Data, init_SMA_12=sma12, init_SMA_24=sma24, r=1.30, v=0)

for data_point in results:
    print(data_point)

''' Strategy Statistics:
Stocks evaluated: 6

Default Conservative Average --> .80036
Optimal Conservative Average --> 1.002855
Buy and hold Average --> .65188

'''