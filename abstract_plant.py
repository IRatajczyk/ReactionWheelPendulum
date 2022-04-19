from abc import ABC, abstractmethod



class PlantParameters(ABC):
    @abstractmethod
    def __init__(self, plant_type: str = " "):
        self.plan_type = plant_type

    @abstractmethod
    def check(self):
        pass


class Plant(ABC):
    @abstractmethod
    def __init__(self, parameters: PlantParameters, *args):
        self.parameters = parameters

    @abstractmethod
    def transition_function(self):
        pass
