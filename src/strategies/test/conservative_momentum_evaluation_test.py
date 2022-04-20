import unittest

from src.strategies.conservative_momentum_strategy_evaluation import evaluate_position


# @Todo: Verify the tests are actually correct


class TestEvaluationFunction(unittest.TestCase):
    def test_eval_function(self):
        """
        Test that it produces the right Position Evaluation of BUY, SELL, or HOLD
        """

        BUY = "BUY"
        SELL = "SELL"
        HOLD = "HOLD"

        # EMA ++ -->  "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2
        # EMA +- -->  "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75
        # EMA -+ -->  "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2
        # EMA -- -->  "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75

        # Section 1 of 4, HOLDING and not Sold at a Loss

        # Test Suite 1 of 16, val1 < target and val2 < target, not loss and not holding

        # Test 1/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA ++ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 2/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA +- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 3/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA -+ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 4/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA -- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 2 of 16, val1 < target and val2 > target, not loss and not holding

        # Test 5/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA ++ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": .9}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 6/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA +- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": .9}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 7/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA -+ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": .9}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 8/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA -- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": .9}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 3 of 16, val1 > target and val2 < target, not loss and not holding

        # Test 9/64: not sold at loss, not HOLDING , val1 > target , val2 < target , EMA ++ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 10/64: not sold at loss, not HOLDING , val1 > target , val2 < target , EMA +- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 11/64: not sold at loss, not HOLDING , val1 > target , val2 < target , EMA -+ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 12/64: not sold at loss, not HOLDING , val1 > target , val2 < target , EMA -- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 4 of 16, val1 > target and val2 > target, not loss and not holding

        # Test 13/64: not sold at loss, not HOLDING , val1 > target , val2 > target , EMA ++ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 14/64: not sold at loss, not HOLDING , val1 > target , val2 > target , EMA +- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 15/64: not sold at loss, not HOLDING , val1 > target , val2 > target , EMA -+ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 16/64: not sold at loss, not HOLDING , val1 > target , val2 > target , EMA -- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Section 2 of 4, HOLDING and Sold at a Loss

        # Test Suite 5 of 16, val1 < target and val2 < target, not loss and not holding

        # Test 13/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA ++ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 14/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA +- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 15/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA -+ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 16/64: not sold at loss, not HOLDING , val1 < target , val2 < target , EMA -- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 6 of 16, val1 < target and val2 > target, not loss and not holding

        # Test 17/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA ++ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 18/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA +- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 19/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA -+ ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 20/64: not sold at loss, not HOLDING , val1 < target , val2 > target , EMA -- ==>
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Section 3 of 4, Not HOLDING and Not Sold at a Loss

        # Section 4 of 4, Not HOLDING and Sold at a Loss

if __name__ == '__main__':
    unittest.main()