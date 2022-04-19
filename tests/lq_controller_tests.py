import unittest

import numpy as np

from lq_controller import LQRController, LQRParameters


class LQControllerTests(unittest.TestCase):
    def test_K_size_scalar(self):
        A = np.array([1])
        B = np.array([1])
        Q = np.array([[1]])
        R = np.array([1])

        LQ = LQRController(LQRParameters(Q, R))
        LQ.tune_controller(A, B, np.array([0, 0]))
        self.assertEqual(LQ.K.shape, (1, 1))

    def test_K_size_A_B_eq_sz(self):
        A = np.array([[1, 0], [0, 1]])
        B = np.array([[1, 0], [0, 1]])
        Q = np.array([[1, 0], [0, 1]])
        R = np.array([[1, 0], [0, 1]])

        LQ = LQRController(LQRParameters(Q, R))
        LQ.tune_controller(A, B, np.array([0, 0]))
        self.assertEqual(LQ.K.shape, (2, 2))

    def test_K_size_flat_B(self):
        A = np.array([[1, 0], [0, 1]])
        B = np.array([[1], [1]])
        Q = np.array([[1, 0], [0, 1]])
        R = np.array([1])

        LQ = LQRController(LQRParameters(Q, R))
        LQ.tune_controller(A, B, np.array([0, 0]))
        self.assertEqual(LQ.K.shape, (1, 2))

    def test_K_size_small_A(self):
        A = np.array([1])
        B = np.array([[1, 1, 1]])
        Q = np.array([[1]])
        R = np.eye(3)

        LQ = LQRController(LQRParameters(Q, R))
        LQ.tune_controller(A, B, np.array([0]))
        self.assertEqual(LQ.K.shape, (3, 1))

    def test_controller_output_size(self):
        A = np.array([[2, 1, 3], [1, 0, 3], [0, 4, 6]])
        B = np.array([[1], [1], [1]])
        Q = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
        R = np.array([[1]])
        LQ = LQRController(LQRParameters(Q, R))
        LQ.tune_controller(A, B)
        u = LQ.get_controller()
        y = u(np.array([0, 0, 0]))
        self.assertEqual(y.shape, (1,))


if __name__ == '__main__':
    unittest.main()
