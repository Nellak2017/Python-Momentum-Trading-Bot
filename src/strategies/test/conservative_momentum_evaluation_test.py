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

        # Section 1 of 3, not HOLDing. Note buy point and sold at loss don't matter, only EMA*.

        # Test Suite 1 of 19, not holding

        # Test 1/40: not HOLDING , EMA ++ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 2/40: not HOLDING , EMA +- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 3/40: not HOLDING , EMA -+ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 4/40: not HOLDING , EMA -- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Section 2 of 3, HOLDING and Sold at a Loss

        # Test Suite 2 of 19, UU, holding, sold at loss, EMA *

        # Test 5/76: HOLDING, sold at loss, UU, EMA ++ ==> SELL

        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 6/76: HOLDING, sold at loss, UU, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 7/76: HOLDING, sold at loss, UU, EMA -+ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 8/76: HOLDING, sold at loss, UU, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 3 of 19, MU, holding, sold at loss, EMA *

        # Test 9/76: HOLDING, sold at loss, MU, EMA ++ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 10/76: HOLDING, sold at loss, MU, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 11/76: HOLDING, sold at loss, MU, EMA -+ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 12/76: HOLDING, sold at loss, MU, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 4 of 19, UM, holding, sold at loss, EMA *

        # Test 13/76: HOLDING, sold at loss, UM, EMA ++ ==> HOLD
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 14/76: HOLDING, sold at loss, UM, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 15/76: HOLDING, sold at loss, UM, EMA -+ ==> HOLD
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 16/76: HOLDING, sold at loss, UM, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 5 of 19, MM, holding, sold at loss, EMA *

        # Test 17/76: HOLDING, sold at loss, MM, EMA ++ ==> HOLD
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 18/76: HOLDING, sold at loss, MM, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 19/76: HOLDING, sold at loss, MM, EMA -+ ==> HOLD
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 20/76: HOLDING, sold at loss, MM, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 6 of 19, DD, holding, sold at loss, EMA *

        # Test 21/76: HOLDING, sold at loss, DD, EMA ++ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 22/76: HOLDING, sold at loss, DD, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 23/76: HOLDING, sold at loss, DD, EMA -+ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 24/76: HOLDING, sold at loss, DD, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 7 of 19, DM, holding, sold at loss, EMA *

        # Test 25/76: HOLDING, sold at loss, DM, EMA ++ ==> HOLD
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 26/76: HOLDING, sold at loss, DM, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 27/76: HOLDING, sold at loss, DM, EMA -+ ==> HOLD
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 28/76: HOLDING, sold at loss, DM, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 8 of 19, MD, holding, sold at loss, EMA *

        # Test 29/76: HOLDING, sold at loss, MD, EMA ++ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 30/76: HOLDING, sold at loss, MD, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 31/76: HOLDING, sold at loss, MD, EMA -+ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 32/76: HOLDING, sold at loss, MD, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 9 of 19, DU, holding, sold at loss, EMA *

        # Test 33/76: HOLDING, sold at loss, DU, EMA ++ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 34/76: HOLDING, sold at loss, DU, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 35/76: HOLDING, sold at loss, DU, EMA -+ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 36/76: HOLDING, sold at loss, DU, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 10 of 19, UD, holding, sold at loss, EMA *

        # Test 37/76: HOLDING, sold at loss, UD, EMA ++ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 38/76: HOLDING, sold at loss, UD, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 39/76: HOLDING, sold at loss, UD, EMA -+ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 40/76: HOLDING, sold at loss, UD, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Section 3 of 3, HOLDING and Sold at a Loss

        # Test Suite 11 of 19, UU, holding, not sold at loss, EMA *

        # Test 41/76: HOLDING, not sold at loss, UU, EMA ++ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 42/76: HOLDING, not sold at loss, UU, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 43/76: HOLDING, not sold at loss, UU, EMA -+ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 44/76: HOLDING, not sold at loss, UU, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 12 of 19, MU, holding, not sold at loss, EMA *

        # Test 45/76: HOLDING, not sold at loss, MU, EMA ++ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 46/76: HOLDING, not sold at loss, MU, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 47/76: HOLDING, not sold at loss, MU, EMA -+ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 48/76: HOLDING, not sold at loss, MU, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 13 of 19, UM, holding, not sold at loss, EMA *

        # Test 49/76: HOLDING, not sold at loss, UM, EMA ++ ==> HOLD
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 50/76: HOLDING, not sold at loss, UM, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 51/76: HOLDING, not sold at loss, UM, EMA -+ ==> HOLD
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 52/76: HOLDING, not sold at loss, UM, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 14 of 19, MM, holding, not sold at loss, EMA *

        # Test 53/76: HOLDING, not sold at loss, MM, EMA ++ ==> HOLD
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 54/76: HOLDING, not sold at loss, MM, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 55/76: HOLDING, not sold at loss, MM, EMA -+ ==> HOLD
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 56/76: HOLDING, not sold at loss, MM, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 15 of 19, DD, holding, not sold at loss, EMA *

        # Test 57/76: HOLDING, not sold at loss, DD, EMA ++ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 58/76: HOLDING, not sold at loss, DD, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 59/76: HOLDING, not sold at loss, DD, EMA -+ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 60/76: HOLDING, not sold at loss, DD, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 16 of 19, DM, holding, not sold at loss, EMA *

        # Test 61/76: HOLDING, not sold at loss, DM, EMA ++ ==> HOLD
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 62/76: HOLDING, not sold at loss, DM, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 63/76: HOLDING, not sold at loss, DM, EMA -+ ==> HOLD
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 64/76: HOLDING, not sold at loss, DM, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.091, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 17 of 19, MD, holding, not sold at loss, EMA *

        # Test 65/76: HOLDING, not sold at loss, MD, EMA ++ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 66/76: HOLDING, not sold at loss, MD, EMA +- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 67/76: HOLDING, not sold at loss, MD, EMA -+ ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 68/76: HOLDING, not sold at loss, MD, EMA -- ==> SELL
        data = {"value_1": 1.091, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 18 of 19, DU, holding, not sold at loss, EMA *

        # Test 69/76: HOLDING, not sold at loss, DU, EMA ++ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 70/76: HOLDING, not sold at loss, DU, EMA +- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 71/76: HOLDING, not sold at loss, DU, EMA -+ ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 72/76: HOLDING, not sold at loss, DU, EMA -- ==> SELL
        data = {"value_1": 1.0355, "value_2": 1.199, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test Suite 19 of 19, UD, holding, not sold at loss, EMA *

        # Test 73/76: HOLDING, not sold at loss, UD, EMA ++ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 74/76: HOLDING, not sold at loss, UD, EMA +- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 75/76: HOLDING, not sold at loss, UD, EMA -+ ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5, "ema12_2": 1.2,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 76/76: HOLDING, not sold at loss, UD, EMA -- ==> SELL
        data = {"value_1": 1.199, "value_2": 1.0355, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5, "ema12_2": 0.75,
                "stock_holding": True, "rec_sold_at_loss": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)


if __name__ == '__main__':
    unittest.main()
