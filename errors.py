class WrongParametersError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class WrongSequenceError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors



