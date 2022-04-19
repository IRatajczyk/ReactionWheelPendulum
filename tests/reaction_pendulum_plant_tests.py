import unittest

import numpy as np

import reaction_pendulum_plant


class MyTestCase(unittest.TestCase):
    def test_output_size(self):

        RP_params = reaction_pendulum_plant.ReactionPendulumParameters()
        RP = reaction_pendulum_plant.ReactionPendulumPlant(RP_params)
        f = RP.transition_function()
        x0 = np.array([0,0,0])
        y = f(x0, np.array([0]))
        z = f(y, np.array([0]))
        self.assertEqual(y.shape, (3,))
        self.assertEqual(z.shape, (3,))


if __name__ == '__main__':
    unittest.main()
