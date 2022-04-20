'''
Date: 19 Apr 2022

Author: Connor Keenum

Description:
    Take in 2 Stock data points and determine whether it is a buy, sell, or hold based on Strategy.

Strategy:
# This strategy will has a constant r,v, and win/loss%
# HOLDing = holding stock, HOLD = hold your current position
    1. Sell if value_2 is +1.r% or -1.v% of buy_point and you are HOLDing the stock, otherwise use Ema Signal below to determine if BUY
    2. If Ema12 is becoming less than Ema24, SELL if you are HOLDing the stock, HOLD if you don't have the stock
    3. If Ema12 is becoming more than Ema24, BUY if you are not HOLDing the stock, HOLD if you have the stock
    4. If you sold at a loss in the last transaction, only BUY iff Ema12 is becoming more than Ema24
    5. If you are HOLDing and Ema12 stays positive over Ema24, SELL if value_2 is >= top_target or value_2 is <= bottom_target , HOLD otherwise
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
'''


def evaluate_position(Data_Point):
    return "BUY"
