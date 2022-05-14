"""
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    Take in 2 Stock data points and determine whether it is a buy, sell, or hold based on Strategy.

Strategy:
    1. Sell if value_2 is +1.r% or -1.v% of buy_point and you are HOLDing the stock, otherwise use Ema Signal
        below to determine if BUY
    2. If Ema12 is becoming less than Ema24, SELL if you are HOLDing the stock, HOLD if you don't have the stock
    3. If Ema12 is becoming more than Ema24, BUY if you are not HOLDing the stock, HOLD if you have the stock
    4. If you are HOLDing and Ema12 stays positive over Ema24, SELL if value_2 is >= top_target or
        value_2 is <= bottom_target , HOLD otherwise
    5. If you are HOLDing and Ema12 stays negative below Ema24, SELL
    6. If you are not HOLDing and Ema12 stays positive over Ema24, BUY
    7. If you are not HOLDing and Ema12 stays negative below Ema24, HOLD (Until BUY Signal)

Input:
    r = 1.1 : (optional) Float (The Positive Sell threshold)
    v = .95 : (optional) Float (The Negative Sell threshold)
    Data_Point : Map {value_1, value_2, ema24_1, ema12_1,ema24_2, ema12_2, status, buy_point}
        (status is current state of stock, holding or Not holding)
        (buy_point is the value where you bought the stock at IF the status is holding too)

Output:
    Trade : Enum String in [BUY , SELL, HOLD]
"""
import math


# @ todo: fix the None return type error
def evaluate_position(data_point: dict, r: float = 1.1, v: float = .95) -> str:

    # Error checking before the program runs

    keys = ["value_1", "value_2", "ema24_1", "ema24_2", "ema12_1", "ema12_2", "stock_holding", "buy_point"]

    if not isinstance(data_point, dict):
        raise TypeError('The Entered Data is not in a Dictionary/Hash Map Format, and therefore can not be parsed.')

    if set(keys) != set(data_point.keys()):
        raise KeyError('Your entered dictionary keys do not match with what a data_point is supposed to have.')

    if not isinstance(data_point["value_1"], float) and not isinstance(data_point["value_1"], int):
        raise TypeError('The Entered value_1 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["value_2"], float) and not isinstance(data_point["value_2"], int):
        raise TypeError('The Entered value_2 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["ema24_1"], float) and not isinstance(data_point["ema24_1"], int):
        raise TypeError('The Entered ema24_1 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["ema24_2"], float) and not isinstance(data_point["ema24_2"], int):
        raise TypeError('The Entered ema24_2 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["ema12_1"], float) and not isinstance(data_point["ema12_1"], int):
        raise TypeError('The Entered ema12_1 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["ema12_2"], float) and not isinstance(data_point["ema12_2"], int):
        raise TypeError('The Entered ema12_2 is not a number, enter a number to fix this error.')

    if not isinstance(data_point["stock_holding"], bool):
        raise TypeError('The Entered stock_holding is not a True/False, enter a boolean to fix this error.')

    if not isinstance(data_point["buy_point"], float) and not isinstance(data_point["buy_point"], int):
        raise TypeError('The Entered buy_point is not a number, enter a number to fix this error.')

    if not isinstance(r, float) and not isinstance(r, int):
        raise TypeError('The Entered r value is not a number, enter a number to fix this error.')

    if not isinstance(v, float) and not isinstance(v, int):
        raise TypeError('The Entered v value is not a number, enter a number to fix this error.')

    # Main execution of the Function

    BUY: str = "BUY"
    SELL: str = "SELL"
    HOLD: str = "HOLD"

    holding: bool = data_point["stock_holding"]
    v2: float = data_point["value_2"]
    top: float = data_point["buy_point"] * r
    bottom: float = data_point["buy_point"] * v
    ema1: float = data_point["ema12_1"] - data_point["ema24_1"]
    ema2: float = data_point["ema12_2"] - data_point["ema24_2"]
    ema_increasing: bool = True if ema1 < 0 < ema2 else False
    ema_decreasing: bool = True if ema1 > 0 > ema2 else False
    ema_double_positive: bool = True if ema1 > 0 and ema2 > 0 and not ema_decreasing and not ema_increasing else False
    ema_double_negative: bool = True if ema1 < 0 and ema2 < 0 and not ema_decreasing and not ema_increasing else False

    if not holding:
        if ema_double_positive:
            return BUY
        elif ema_decreasing:
            return HOLD
        elif ema_increasing:
            return BUY
        elif ema_double_negative:
            return HOLD
        else:
            return HOLD

    elif holding:
        if v2 > top or math.isclose(v2, top) or v2 < bottom or math.isclose(v2, bottom):
            return SELL
        elif ema_decreasing:
            return SELL
        elif ema_increasing:
            return HOLD
        elif ema_double_negative:
            return SELL
        else:
            return HOLD

    else:
        return HOLD