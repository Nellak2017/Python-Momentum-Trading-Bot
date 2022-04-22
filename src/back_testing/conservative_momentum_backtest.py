"""
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    "Momentum investing" means investing in the stocks that have increased in price the most.
    For this back_testing, we're going to analyze a given stock and output the profitability of the strategy.

Strategy:
    Sell at +10% or -5%, if -5% sell then wait until momentum indicator
    to buy. We will use momentum_strategy_evaluation to determine when to buy/sell/hold at any point.

Input:
    Start_Date : Date
    End_Date : Date
    Interval : Time (query every 1d , 1h, 10min, 1month, ...)
    Data : (Map? DataFrame? List?)
    Initially_Holding = False : (Optional) Boolean

Output: (Will be displayed using strat_display)
    store : [Map] (All the positions meta-data after everything is over. Last element has profitability)
"""

'''
# unit tests will cover: X indicators (in another file), bayesian_belief_updater (in another file), 
#                        rv_estimator (in another file)

input = stock_initially_holding = False, 

models: defined as belief in wins/losses, constant 50%/50% for this, thus it will always be worth it to try 
store: defined as r,v for this, constant r,v value for this, thus upper and lower target constant

for each data_point in data_set:
    X calculate indicators using provided indicator function
    X compose eval_dto using indicators
    X evaluate position, passing in dto and store data
    X store meta_data about position (win/loss, profit, date/time of trade, buy/sell/hold, ...)
    X update models (update r,v estimates, update win/loss beliefs)
    (in main, use the model AND evaluation function to output Buy and Hold, Sell and Hold, Sell and Buy, and This Stock 
        isn't profitable anymore)

return store    

'''

'''
momentum_strategy_DTO = 
    {"value_1":{from API}, "value_2":{from API}, "ema24_1":{calculated}, "ema24_2":{calculated}, 
    "ema12_1":{calculated}, "ema12_2":{calculated}, "stock_holding":{initial from input, after determined by algorithm}, 
    "buy_point":{initial from input, after determined by algorithm}}

store = 
    [
        1: {
            ticker: Stock name
            date: ISO Date/time
            value: Stock Value at this point
            holding_stock: False if you don't have the stock True otherwise
            current_profitability_multiplier: 1 starting off, then whatever is computed later
            position_evaluation: "BUY", "SELL", or "HOLD"
            position_two_step_evaluation: "BUY and HOLD", "SELL and HOLD", "SELL and BUY", "HOLD"     
        },
        ...
    ]

input Data =
    [
        ISO Date/time: {
            ticker: Stock name
            date: ISO Date/time
            value: Stock Value at this point    
        },
        ...
    ]

'''
import src.strategies.indicators.ema as ema
import src.strategies.evaluation_functions.momentum_strategy_evaluation as mse

# @todo: unit test this function

def conservative_momementum_backtest(data_set, init_SMA_24, init_SMA_12, initially_holding=False) -> list:
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    BH = "BUY and HOLD"
    SH = "SELL and HOLD"
    SB = "SELL and BUY"
    HH = "HOLD and HOLD"
    position_two_step_evaluation = HH
    store = []                              # Holds all the Meta-data for each position, stored for display purposes
    buy_point = data_set[1]["value"]        # The value that you bought a stock at
    sell_point = data_set[1]["value"]       # The value that you sold a stock at
    profitability_multiplier = 1            # Updated iteratively starting at 1
    r = 1.1                                 # Upper Sell Price Target
    v = .95                                 # Lower Sell Price Target
    holding = initially_holding             # Changes based off evaluation function
    EMA_24_1 = init_SMA_24                  # Has to start as init_SMA_24
    EMA_12_1 = init_SMA_12                  # Has to start as init_SMA_12
    next_position_evaluation: str = HOLD    # Next Evaluation, used for 2 step evaluation
    position_evaluation: str = HOLD         # Initial Evaluation defaults to HOLD

    for data_index in range(len(data_set)-3):
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
        position_evaluation = mse.evaluate_position(data_point=eval_dto)

        EMA_24_1 = EMA_24_2  # Updated with New Previous Ema values
        EMA_12_1 = EMA_12_2  # Updated with New Previous Ema values
        EMA_24_2 = ema.ema(prev_ema=EMA_24_2, data_point=value_1, days=24)
        EMA_12_2 = ema.ema(prev_ema=EMA_12_2, data_point=value_1, days=12)

        # update related variables for the store
        if position_evaluation == BUY:
            #next_position_evaluation = BUY
            buy_point = value_2
            profitability_multiplier *= (sell_point / buy_point)
            holding = True
        elif position_evaluation == SELL:
            #next_position_evaluation = SELL
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
        next_position_evaluation = mse.evaluate_position(data_point=eval_dto_next)

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

results = conservative_momementum_backtest(data_set=mock_data_set, init_SMA_24=sma24, init_SMA_12=sma12)

for data_point in results:
    print(data_point)























