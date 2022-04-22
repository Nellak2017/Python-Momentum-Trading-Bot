"""
Date: 21 Apr 2022

Author: Connor Keenum

Description:
    Take in a data point with meta-data and output the exponential moving average for a given day range.
    You need at least 2 closing prices for this Indicator to Work.

Formula:
    EMA = Closing Price * multiplier + EMA(previous day Closing Price) * (1-multiplier)
        EMA(previous day Closing Price) -> Is this function, unless if it is start of interval, then it is sma at that
            point
        multiplier = (Smoothing / (1 + Days))
        Smoothing -> Typically taken to be 2
        Closing Price Today -> given by API
        Closing Price Yesterday -> given by API
        Days -> given as input (I.E. EMA_24(NVIDIA_Data))

Meta-Data Needed:
    Closing Price Today --> Provided by API or RNG
    EMA(yesterday) --> Basically the last EMA Computed, if start of interval it will be SMA from API / generated data

Input:
    Smoothing = 2 : (optional) Float (The Smoothing Factor)
    Current_EMA : Float (The Current EMA previously computed)
    Data_Point : Float (Closing Price Today)
    Days : Float (The Number of days in which to perform the EMA)

Output:
    EMA : Float (The Exponential Moving Average for number of days, given meta-data)
"""


def ema(prev_ema, data_point, days, smoothing=2):
    if not isinstance(prev_ema, float) and not isinstance(prev_ema, int):
        raise TypeError('The Entered Previous Ema value is not a number. Enter a valid number to compute ema.')
    if not isinstance(data_point, float) and not isinstance(data_point, int):
        raise TypeError('The Entered data_point value is not a number. Enter a valid number to compute ema.')
    if not isinstance(days, float) and not isinstance(days, int):
        raise TypeError('The Entered days value is not a number. Enter a valid number to compute ema.')
    if not isinstance(smoothing, float) and not isinstance(smoothing, int):
        raise TypeError('The Entered smoothing value is not a number. Enter a valid number to compute ema.')
    multiplier = (smoothing / (1 + days))
    return data_point * multiplier + prev_ema * (1 - multiplier)
