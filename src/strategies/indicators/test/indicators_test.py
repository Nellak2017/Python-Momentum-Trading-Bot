import unittest

from src.strategies.indicators.ema import ema


class TestIndicators(unittest.TestCase):

    def test_ema_function(self):
        """
        Test that it produces the right Exponential Moving Averages
        """

        '''
        Type/Key Testing
        '''

        # Type Test 1
        prev_ema = 1.3903
        data_point = 2
        days = "string"
        self.assertRaises(TypeError, ema, prev_ema=prev_ema, data_point=data_point, days=days)

        # Type Test 2
        prev_ema = 1.3903
        data_point = 1 + 1j
        days = 2
        self.assertRaises(TypeError, ema, prev_ema=prev_ema, data_point=data_point, days=days)

        # Type Test 3
        prev_ema = {"Key": 1, "1": .4}
        data_point = 1 + 1j
        days = 2
        self.assertRaises(TypeError, ema, prev_ema=prev_ema, data_point=data_point, days=days)

        '''
        Value Testing
        '''

        # Value Test 1, ema_3(1.3903,2,3)

        prev_ema = 1.3903
        data_point = 2
        days = 3
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.6951, result, places=4)

        # Value Test 2, ema_3(1.2444,1,3)

        prev_ema = 1.2444
        data_point = 1.6
        days = 3
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.4222, result, places=4)

        # Value Test 3, ema_3(1.55,2,3)

        prev_ema = 1.55
        data_point = 2
        days = 3
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.7750, result, places=4)

        # Value Test 4, ema_12(1.6192,2,12)

        prev_ema = 1.6192
        data_point = 1.58
        days = 12
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.6132, result, places=4)

        # Value Test 5, ema_12(1.4968,1,12)

        prev_ema = 1.4968
        data_point = 1.7
        days = 12
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.5281, result, places=4)

        # Value Test 6, ema_12(1.55,2,12)

        prev_ema = 1.55
        data_point = 2
        days = 12
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.6192, result, places=4)

        # Value Test 7, ema_12(1.7474,1.6,12)

        prev_ema = 1.7474
        data_point = 1.6
        days = 12
        result = ema(prev_ema=prev_ema, data_point=data_point, days=days)
        self.assertAlmostEqual(1.7247, result, places=4)


if __name__ == '__main__':
    unittest.main()
