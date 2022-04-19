from abc import ABC, abstractmethod


class ControllerParameters(ABC):
    @abstractmethod
    def __init__(self, controller_type: str):
        self.controller_type = controller_type

    @abstractmethod
    def check(self):
        pass


class Controller(ABC):
    @abstractmethod
    def __init__(self, parameters: ControllerParameters):
        self.parameters = parameters

    @abstractmethod
    def tune_controller(self, *args):
        pass

    @abstractmethod
    def get_controller(self):
        pass
