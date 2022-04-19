from types import LambdaType, FunctionType
import numpy as np
import abstract_controller
import errors

H: str = "Hybrid controller"


class HybridControllerParameters(abstract_controller.ControllerParameters):
    def __init__(self, ref_point_controller: [LambdaType | FunctionType],
                 approach_controller: [LambdaType | FunctionType], condition: str = "position"):
        super().__init__(controller_type=H)
        self.feasible_conditions = ("position", "energy", "custom")
        self.ref_point_controller = ref_point_controller
        self.approach_controller = approach_controller
        self.condition = condition
        self.check()

    def check(self):
        if self.condition not in self.feasible_conditions:
            raise errors.WrongParametersError(f"Condition should be one of these:{self.feasible_conditions}")


class HybridController(abstract_controller.Controller):
    def __init__(self, parameters: HybridControllerParameters):
        super().__init__(parameters=parameters)
        self.controller = None

    def tune_controller(self, threshold, condition=None):
        f = self.parameters.ref_point_controller
        g = self.parameters.approach_controller
        if self.parameters.condition == "position":
            self.controller = lambda x: f(x) * int(np.cos(x[1]) < threshold) + g(x) * (
                        1 - int(np.cos(x[1]) < threshold))
        elif self.parameters.condition == "energy":
            E = lambda x: np.sin(x[1]) + np.cos(x[0]) ** 2  # TODO: Improve
            self.controller = lambda x: f(x) * int(E < threshold) + g(x) * (1 - int(E < threshold))
        elif self.parameters.condition == "custom":
            self.controller = lambda x: self.parameters.f(x) \
                if condition(x) else self.parameters.g(x)
        else:
            raise errors.WrongParametersError("No such condition avaliable!")

    def get_controller(self):
        if self.controller is None:
            raise errors.WrongSequenceError("Before getting a controller it is necessary to fine-tune it!")
        else:
            return self.controller
