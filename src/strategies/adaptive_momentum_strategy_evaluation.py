'''
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    "Momentum investing" means investing in the stocks that have increased in price the most.
    This project will use a similar strat as in conservative_momentum, but it will learn the right sell value and update
    it's model of the stock iteratively.
    For this project, we're going to analyze a given stock and output the profitability of the strategy.

Input:
    Start_Date : Date
    End_Date : Date
    Interval : Time (query every 1d , 1h, 10min, 1month, ...)
    Data : (Map? DataFrame? List?)

Output:

'''

import numpy as np
import pandas as pd
import requests