'''
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    "Momentum investing" means investing in the stocks that have increased in price the most.
    For this project, we're going to analyze a given stock and output the profitability of the strategy.

Strategy:
    1. At start of interval, buy with all money alotted
    2.
    Sell at +10% or -5%, if -5% sell then wait until momentum indicator
    to buy.

Input:
    Start_Date : Date
    End_Date : Date
    Interval : Time (query every 1d , 1h, 10min, 1month, ...)
    Data : (Map? DataFrame? List?)
    Money : Float

Output: (Will be displayed using strat_display)
    Profitability : Float (1.0 means break even, <1.0 means net loss multiplier, >1.0 means net gain multiplier)
    End_money : Float
'''

import numpy as np
import pandas as pd
import requests
