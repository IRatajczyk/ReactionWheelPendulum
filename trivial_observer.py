import abstract_observer
import errors

TO: str = "Trivial observer"


class TrivialObserverParameters(abstract_observer.ObserverParameters):
    def __init__(self):
        super().__init__(observer_type=TO)

    def check(self):
        if self.observer_type is None:
            raise errors.WrongParametersError("Wrong parameters!")


class TrivialObserver(abstract_observer.Observer):
    def __init__(self, parameters: TrivialObserverParameters):
        super().__init__(parameters=parameters)

    def get_observation(self):
        return lambda state: state
