import numpy as np
from types import LambdaType, FunctionType
from control import lqr

import abstract_controller
import errors


class LQRParameters(abstract_controller.ControllerParameters):
    def __init__(self, Q: np.ndarray, R: np.ndarray, N=None, S=None):
        super().__init__(controller_type="LQ")
        self.Q = Q
        self.R = R
        self.N = N
        self.S = S
        self.check()

    def check(self):
        if self.Q.shape[0] != self.Q.shape[1]:
            raise errors.WrongParametersError("Q should be a square matrix!")
        if len(self.R.shape) == 2 and self.R.shape[0] != self.R.shape[1]:
            raise errors.WrongParametersError("R should be a square matrix!")
        if self.N is not None:
            if self.Q.shape[1] != self.N.shape[0]:
                raise errors.WrongParametersError("N matrix has wrong shape!")
            if self.R.shape[1] != self.N.shape[0]:
                raise errors.WrongParametersError("N matrix has wrong shape!")


class LQRController(abstract_controller.Controller):
    def __init__(self, parameters: LQRParameters):
        super().__init__(parameters=parameters)
        self.K = None
        self.S = None
        self.E = None
        self.x0 = None

    def tune_controller(self, A, B, x0=np.array([0, 0, 0])) -> None:
        self.x0 = x0
        self.K, self.S, self.E = lqr(A, B, self.parameters.Q, self.parameters.R)

    def get_controller(self) -> [LambdaType | FunctionType]:
        if self.K is None:
            raise errors.WrongSequenceError("Before getting a controller it is necessary to fine-tune it!")
        else:
            return lambda x: -self.K @ (x-self.x0)
