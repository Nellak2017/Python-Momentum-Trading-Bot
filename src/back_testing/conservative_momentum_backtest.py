import src.strategies.indicators.ema as ema
import src.strategies.evaluation_functions.momentum_strategy_evaluation as mse

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
