from typing import Optional
from types import LambdaType, FunctionType

import numpy as np

import abstract_plant
import errors

RP: str = "ReactionPendulum"


class ReactionPendulumParameters(abstract_plant.PlantParameters):
    def __init__(self, ksi: float = .03, omega_0: float = 2.36, K: float = 529.798, k_p: float = -4.3434,
                 H: float = .0022, T: float = 0.001, control_saturation: Optional[float] = None) -> None:
        """

        :param ksi: float,
        :param omega_0: float,
        :param K: float,
        :param k_p: float,
        :param H: float,
        :param T: float, sampling time
        :param control_saturation: Optional[float], saturation threshold
        """
        super().__init__(plant_type=RP)
        self.ksi: float = ksi
        self.omega_0: float = omega_0
        self.K: float = K
        self.k_p: float = k_p
        self.H: float = H
        self.T: float = T
        self.control_saturation: Optional[float] = control_saturation
        self.check()

    def check(self) -> None:
        """
        Should any of parameters in constructor be inconsistent with physical model the very method will raise a
        proper error.
        :return: None
        """
        if self.omega_0 < 0:
            raise errors.WrongParametersError(
                f"Omega parameter should be greater than 0, currently omega_0 = {self.omega_0}")
        if self.control_saturation <= 0:
            raise errors.WrongParametersError(
                f"Saturation parameter should be greater than 0, currently threshold = {self.omega_0}")


class ReactionPendulumPlant(abstract_plant.Plant):

    def __init__(self, parameters: ReactionPendulumParameters):
        super().__init__(parameters=parameters)
        self.A_lin = None
        self.B_lin = None
        self.saturation = lambda u: np.maximum(np.minimum(u, self.parameters.control_saturation),
                                               -self.parameters.control_saturation) \
            if self.parameters.control_saturation is not None else None

    def transition_function(self, saturated: bool = False) -> [LambdaType | FunctionType]:
        """
        Method dedicated to obtaining full dynamics of a system.
        :param saturated: decides whether control signal should be saturated
        :return: function performing continuous time transfer function Dx = f(x,u)
        """
        A = np.array([[-2 * self.parameters.ksi * self.parameters.omega_0, 0, -self.parameters.k_p * self.parameters.H],
                      [1, 0, 0],
                      [0, 0, -self.parameters.K * self.parameters.H]])
        B = np.array([[self.parameters.k_p], [0], [self.parameters.K]])
        w = -self.parameters.omega_0 * self.parameters.omega_0
        if saturated:
            return lambda x, u: A @ x + np.array([w * np.sin(x[1]), 0, 0]) + B @ self.saturation(u)
        else:
            return lambda x, u: A @ x + np.array([w * np.sin(x[1]), 0, 0]) + B @ u

    def linear_transition_function(self, saturated: bool = False) -> [LambdaType | FunctionType]:
        """
        Method dedicated to obtaining linear dynamics of a system.
        Before getting results, it is the very necessity to perform linearize() method.
        :param saturated: bool decides whether control signal should be saturated
        :return: function performing continuous time transfer function Dx = f(x,u)
        """
        if self.A_lin is None or self.B_lin is None:
            raise errors.WrongSequenceError("Before getting linear transition function please linearize the model!")
        elif saturated:
            if self.saturation is None:
                raise errors.WrongSequenceError("It is impossible to saturate unsaturated control signal!")
            else:
                return lambda x, u: self.A_lin @ x + self.B_lin @ self.saturation(u)
        else:
            return lambda x, u: self.A_lin @ x + self.B_lin @ u

    def linearize(self, x0: np.ndarray):
        """
        Method dedicated to linearization of a system and obtaining state and control linear matrices.
        :param x0: point in state space at which system will be linearized
        :return: A (state) and B (control) matrices such that: Dx = Ax + Bu
        """
        x = -self.parameters.omega_0 * self.parameters.omega_0 * np.cos(x0[1])
        self.A_lin = np.array(
            [[-2 * self.parameters.ksi * self.parameters.omega_0, x, -self.parameters.k_p * self.parameters.H],
             [1, 0, 0],
             [0, 0, -self.parameters.K * self.parameters.H]])
        self.B_lin = np.array([[self.parameters.k_p], [0], [self.parameters.K]])
        return self.A_lin, self.B_lin
