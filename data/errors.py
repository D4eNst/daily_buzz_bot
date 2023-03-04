
class InsufficientFundsError(Exception):
    """ Raised when there is not enough money on the balance to write off """

    def __init__(self, message="There is not enough money on the balance to write off", error_code=402):
        self.message = message
        self.code = error_code
        super().__init__(message)


class SubscriptionNotFoundError(Exception):
    """"""
    def __init__(self, message="", error_code=407):
        self.message = message
        self.code = error_code
        super().__init__(message)
