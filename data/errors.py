
class InsufficientFundsError(Exception):
    """ Raised when there is not enough money on the balance to write off """

    def __init__(self, message="There is not enough money on the balance to write off", error_code=402):
        self.message = message
        self.code = error_code
        super().__init__(message)


class SubscriptionNotFoundError(Exception):
    """ Raised when subscription is not found in database """
    def __init__(self, message="Subscription is not found in database", error_code=404):
        self.message = message
        self.code = error_code
        super().__init__(message)


class MinReplenishmentAmountError(Exception):
    """ Raised when quantity < min replenishment amount """

    def __init__(self, message="Subscription is not found in database", error_code=406):
        self.message = message
        self.code = error_code
        super().__init__(message)
