from abc import ABC, abstractmethod


class ObserverParameters(ABC):
    @abstractmethod
    def __init__(self, observer_type: str):
        self.observer_type = observer_type

    @abstractmethod
    def check(self):
        pass


class Observer(ABC):
    @abstractmethod
    def __init__(self, parameters: ObserverParameters):
        self.parameters = parameters

    @abstractmethod
    def get_observation(self):
        pass


