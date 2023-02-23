import datetime


def get_subscribe(tg_id):
    sub_date = datetime.date(2023, 1, 1)
    sub_period = 12
    return {
        "date": sub_date,
        "period": sub_period
    }


class User:
    def __init__(self, tg_id, balance=0, total_buy=0, total_sub=0, status="Bronze", subscribe=False) -> None:
        self._tg_id = tg_id
        self.balance = balance
        self.total_buy = total_buy
        self.total_sub = total_sub
        self.status = status
        self.subscribe = subscribe
        self.subscribe_date = datetime.date(2000, 1, 1)
        self.subscribe_period = 0

        if self.subscribe:
            sub = get_subscribe(tg_id)
            self.subscribe_date = sub["date"]
            self.subscribe_period = sub["period"]

    @property
    def tg_id(self) -> int:
        return self._tg_id

    def replenish_balance(self, quantity) -> None:
        self.balance += quantity

    def buy(self, price, period) -> bool:
        if self.balance - price >= 0:
            self.balance = self.balance - price
            if not self.subscribe:
                self.subscribe = True
                self.subscribe_date = datetime.date.today()
                self.subscribe_period = period
            else:
                pass
            return True
        return False


print(datetime.date.today() - datetime.date(2023, 1, 1))
