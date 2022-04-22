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
    Money : Float

Output: (Will be displayed using strat_display)
    Profitability : Float (1.0 means break even, <1.0 means net loss multiplier, >1.0 means net gain multiplier)
    End_money : Float
"""

'''
# unit tests will cover: compose_dto, indicators (in another file), bayesian_belief_updater (in another file), 
#                        rv_estimator (in another file)

def compose_dto(...): defined

models: defined
store: defined

for each data_point in data_set:
    calculate indicators using provided indicator function
    compose eval_dto using indicators
    evaluate position
    store meta_data about position (win/loss, profit, date/time of trade, buy/sell/hold, ...)
    update models (update r,v estimates, update win/loss beliefs)
    (in main, use the model AND evaluation function to output Buy and Hold, Sell and Hold, Sell and Buy, and This Stock 
        isn't profitable anymore)

return store    

'''





