import unittest

import numpy as np

import custom_rule_controller


class MyTestCase(unittest.TestCase):
    def test_output_shape(self):
        CRC_params = custom_rule_controller.CustomRuleControllerParameters()
        RBC = custom_rule_controller.RuleController(CRC_params)

        RBC.tune_controller()

        f = RBC.get_controller()
        x0 = np.array([0, 0, 0])
        y = f(x0)
        self.assertEqual(y.shape, (1,))

if __name__ == '__main__':
    unittest.main()
