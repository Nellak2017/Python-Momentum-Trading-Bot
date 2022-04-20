"""
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    Take in 2 Stock data points and determine whether it is a buy, sell, or hold based on Strategy.

Strategy:
# This strategy will has a constant r,v, and win/loss%
# HOLDing = holding stock, HOLD = hold your current position
    1. Sell if value_2 is +1.r% or -1.v% of buy_point and you are HOLDing the stock, otherwise use Ema Signal
        below to determine if BUY
    2. If Ema12 is becoming less than Ema24, SELL if you are HOLDing the stock, HOLD if you don't have the stock
    3. If Ema12 is becoming more than Ema24, BUY if you are not HOLDing the stock, HOLD if you have the stock
    4. If you sold at a loss in the last transaction, only BUY iff Ema12 is becoming more than Ema24
    5. If you are HOLDing and Ema12 stays positive over Ema24, SELL if value_2 is >= top_target or
        value_2 is <= bottom_target , HOLD otherwise
    6. If you are HOLDing and Ema12 stays negative below Ema24, SELL
    7. If you are not HOLDing and Ema12 stays positive over Ema24, BUY
    8. If you are not HOLDing and Ema12 stays negative below Ema24, HOLD (Until BUY Signal)

Input:
    r : Float (The Positive Sell threshold)
    v : Float (The Negative Sell threshold)
    Data_Point : Map {value_1, value_2, ema24_1, ema12_1,ema24_2, ema12_2, status ,rec_sold_at_loss, buy_point}
        (status is current state of stock, holding or Not holding)
        (buy_point is the value where you bought the stock at IF the status is holding too)

Output:
    Trade : Enum String in [BUY , SELL, HOLD]
"""

'''
EMA ++ -->  "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2
EMA +- -->  "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75
EMA -+ -->  "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2
EMA -- -->  "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75
'''


def evaluate_position(data_point: dict):
    # ema12 - ema24 = +/-
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

    sold_at_loss = data_point["rec_sold_at_loss"]
    holding = data_point["stock_holding"]
    ema1 = data_point["ema12_1"] - data_point["ema24_1"]
    ema2 = data_point["ema12_2"] - data_point["ema24_2"]
    ema_increasing = True if ema1 < 0 < ema2 else False
    ema_decreasing = True if ema1 > 0 > ema2 else False
    ema_double_positive = True if ema1 > 0 and ema2 > 0 and not ema_decreasing and not ema_increasing else False
    ema_double_negative = True if ema1 < 0 and ema2 < 0 and not ema_decreasing and not ema_increasing else False

    if not holding:
        if ema_double_positive:
            return BUY
        elif ema_decreasing:
            return HOLD
        elif ema_increasing:
            return BUY
        elif ema_double_negative:
            return HOLD

    elif holding and sold_at_loss:
        pass

    elif holding and not sold_at_loss:
        pass

    else:
        return HOLD  # When in doubt, HOLD
