import unittest

from src.strategies.evaluation_functions.momentum_strategy_evaluation import evaluate_position


class TestEvaluationFunction(unittest.TestCase):
    def test_eval_function(self):
        """
        Test that it produces the right Position Evaluation of BUY, SELL, or HOLD
        """

        BUY = "BUY"
        SELL = "SELL"
        HOLD = "HOLD"

        r = 1.1
        v = .95
        buy_point = 1.09

        '''
        Type/Key Testing
        '''

        # Type Test 1
        data = {"value_1": "String value", "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        self.assertRaises(TypeError, evaluate_position, data_point=data)

        # Type Test 2
        data = {"value_1": 1, "value_2": "Foo", "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        self.assertRaises(TypeError, evaluate_position, data_point=data)

        # Type Error Test 3
        data = 1
        self.assertRaises(TypeError, evaluate_position, data_point=data)

        # Key Error Test 4
        data = {"value_1": 1, "value_2": "Foo", "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True}
        self.assertRaises(KeyError, evaluate_position, data_point=data)

        # Type Test 5
        data = {"value_1": 1, "value_2": 2, "ema24_1": "Hello", "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        self.assertRaises(TypeError, evaluate_position, data_point=data)

        # Type Test 7
        data = {"value_1": 1, "value_2": 2, "ema24_1": .5, "ema24_2": {}, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        self.assertRaises(TypeError, evaluate_position, data_point=data)

        # Key Error Test 8
        data = {"value_1": 1, "value_2": 2, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09, "Extra": 1.20}
        self.assertRaises(KeyError, evaluate_position, data_point=data)

        # Combination Test 9
        data = {"value_1": 1, "value_2": 2, "ema24_1": .5, "ema24_2": {}, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09, "Extra": 1.20}
        self.assertRaises(Exception, evaluate_position, data_point=data)

        '''
        Function Return Value Testing
        '''

        # Section 1 of 2, not HOLDING. Note buy point and sold at loss don't matter, only EMA*.

        # Test Suite 1 of 19, not holding

        # Test 1/40: not HOLDING , EMA ++ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": .75, "ema12_1": 1, "ema12_2": 1.2,
                "stock_holding": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 2/40: not HOLDING , EMA +- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": .5, "ema24_2": 1.2, "ema12_1": 1, "ema12_2": .75,
                "stock_holding": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 3/40: not HOLDING , EMA -+ ==> BUY
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": .75, "ema12_1": .5, "ema12_2": 1.2,
                "stock_holding": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(BUY, result)

        # Test 4/40: not HOLDING , EMA -- ==> HOLD
        data = {"value_1": 1, "value_2": 1.09, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": .5, "ema12_2": .75,
                "stock_holding": False, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Section 2 of 2, HOLDING

        # Test Suite 2 of 10, UU, holding, EMA *

        # Test 5/40: HOLDING, UU, EMA ++ ==> SELL
        data = {"value_1": r * buy_point, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 6/40: HOLDING, UU, EMA +- ==> SELL
        data = {"value_1": r * buy_point, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 7/40: HOLDING, UU, EMA -+ ==> SELL
        data = {"value_1": r * buy_point, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 8/40: HOLDING, UU, EMA -- ==> SELL
        data = {"value_1": r * buy_point, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 3 of 10, MU, holding, EMA *

        # Test 9/40: HOLDING, MU, EMA ++ ==> SELL
        data = {"value_1": buy_point + .001, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 10/40: HOLDING, MU, EMA +- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 11/40: HOLDING, MU, EMA -+ ==> SELL
        data = {"value_1": buy_point + .001, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 12/40: HOLDING, MU, EMA -- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 4 of 10, UM, holding, EMA *

        # Test 13/40: HOLDING, UM, EMA ++ ==> HOLD
        data = {"value_1": r * buy_point, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 14/40: HOLDING, UM, EMA +- ==> SELL
        data = {"value_1": r * buy_point, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 15/40: HOLDING, UM, EMA -+ ==> HOLD
        data = {"value_1": r * buy_point, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 16/40: HOLDING, UM, EMA -- ==> SELL
        data = {"value_1": r * buy_point, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 5 of 10, MM, holding, EMA *

        # Test 17/40: HOLDING, MM, EMA ++ ==> HOLD
        data = {"value_1": buy_point + .001, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 18/40: HOLDING, MM, EMA +- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 19/40: HOLDING, MM, EMA -+ ==> HOLD
        data = {"value_1": buy_point + .001, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 20/40: HOLDING, MM, EMA -- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 6 of 10, DD, holding, EMA *

        # Test 21/40: HOLDING, DD, EMA ++ ==> SELL
        data = {"value_1": v * buy_point, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 22/40: HOLDING, DD, EMA +- ==> SELL
        data = {"value_1": v * buy_point, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 23/40: HOLDING, DD, EMA -+ ==> SELL
        data = {"value_1": v * buy_point, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 24/40: HOLDING, DD, EMA -- ==> SELL
        data = {"value_1": v * buy_point, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 7 of 10, DM, holding, EMA *

        # Test 25/40: HOLDING, DM, EMA ++ ==> HOLD
        data = {"value_1": v * buy_point, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 26/40: HOLDING, DM, EMA +- ==> SELL
        data = {"value_1": v * buy_point, "value_2": buy_point + .001, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 27/40: HOLDING, DM, EMA -+ ==> HOLD
        data = {"value_1": v * buy_point, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(HOLD, result)

        # Test 28/40: HOLDING, DM, EMA -- ==> SELL
        data = {"value_1": v * buy_point, "value_2": buy_point + .001, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 8 of 10, MD, holding, EMA *

        # Test 29/40: HOLDING, MD, EMA ++ ==> SELL
        data = {"value_1": buy_point + .001, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 30/40: HOLDING, MD, EMA +- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 31/40: HOLDING, MD, EMA -+ ==> SELL
        data = {"value_1": buy_point + .001, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 32/40: HOLDING, MD, EMA -- ==> SELL
        data = {"value_1": buy_point + .001, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 9 of 10, DU, holding, EMA *

        # Test 33/40: HOLDING, DU, EMA ++ ==> SELL
        data = {"value_1": v * buy_point, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 34/40: HOLDING, DU, EMA +- ==> SELL
        data = {"value_1": v * buy_point, "value_2": r * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 35/40: HOLDING, DU, EMA -+ ==> SELL
        data = {"value_1": v * buy_point, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 36/40: HOLDING, DU, EMA -- ==> SELL
        data = {"value_1": v * buy_point, "value_2": r * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test Suite 10 of 10, UD, holding, EMA *

        # Test 37/40: HOLDING, UD, EMA ++ ==> SELL
        data = {"value_1": r * buy_point, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 0.75, "ema12_1": 1,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 38/40: HOLDING, UD, EMA +- ==> SELL
        data = {"value_1": r * buy_point, "value_2": v * buy_point, "ema24_1": 0.5, "ema24_2": 1.2, "ema12_1": 1,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 39/40: HOLDING, UD, EMA -+ ==> SELL
        data = {"value_1": r * buy_point, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 0.75, "ema12_1": 0.5,
                "ema12_2": 1.2,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)

        # Test 40/40: HOLDING, UD, EMA -- ==> SELL
        data = {"value_1": r * buy_point, "value_2": v * buy_point, "ema24_1": 1, "ema24_2": 1.2, "ema12_1": 0.5,
                "ema12_2": 0.75,
                "stock_holding": True, "buy_point": 1.09}
        result = evaluate_position(data)
        self.assertEqual(SELL, result)


if __name__ == '__main__':
    unittest.main()
