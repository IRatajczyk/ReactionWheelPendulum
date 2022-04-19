import unittest

import numpy as np

import custom_rule_controller
import hybrid_controller
import lq_controller
import reaction_pendulum_plant


class MyTestCase(unittest.TestCase):
    def test_something(self):
        RP_params = reaction_pendulum_plant.ReactionPendulumParameters()
        RP = reaction_pendulum_plant.ReactionPendulumPlant(RP_params)
        x_ = np.array([0, np.pi, 0])
        Q = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        R = np.array([1])

        LQ_params = lq_controller.LQRParameters(Q, R)
        LQ = lq_controller.LQRController(LQ_params)

        RBC_params = custom_rule_controller.CustomRuleControllerParameters()
        RBC = custom_rule_controller.RuleController(RBC_params)
        A, B = RP.linearize(x_)
        LQ.tune_controller(A, B, x_)
        u = LQ.get_controller()
        RBC.tune_controller()
        rb = RBC.get_controller()

        HC_params = hybrid_controller.HybridControllerParameters(u, rb)
        HC = hybrid_controller.HybridController(HC_params)
        HC.tune_controller(threshold=0)
        hc = HC.get_controller()
        y = hc(np.array([1, 1, 1]))
        z = hc(np.array([1, -1, 1]))

        self.assertEqual(y.shape, (1,))
        self.assertEqual(z.shape, (1,))



if __name__ == '__main__':
    unittest.main()
