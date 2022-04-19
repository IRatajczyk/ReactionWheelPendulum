import errors
from typing import Optional

import numpy as np

import abstract_controller
import errors

RBC: str = "Rule based controller"


class CustomRuleControllerParameters(abstract_controller.ControllerParameters):
    def __init__(self, max_value: float = 1.0):
        super().__init__(controller_type=RBC)
        self.max_value: float = max_value
        self.check()

    def check(self):
        if self.max_value <= 0:
            raise errors.WrongParametersError(
                f"Value of controller should be positive! (currently max_val = {self.max_value}")


class RuleController(abstract_controller.Controller):
    def __init__(self, parameters: CustomRuleControllerParameters):
        super().__init__(parameters=parameters)
        self.controller = None
        self.threshold: Optional[float] = None

    def tune_controller(self):
        self.threshold = np.array([self.parameters.max_value])

    def get_controller(self):
        if self.threshold is None:
            raise errors.WrongSequenceError("Before getting a controller it is necessary to fine-tune it!")
        else:
            return lambda state: self.threshold if state[0] < 0 else -self.threshold
