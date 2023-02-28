import datetime


def get_subscribe(tg_id):
    sub_start = datetime.date(2023, 1, 1)
    sub_period = 12
    return {
        "date": sub_start,
        "period": round(sub_period*30.4)
    }


class Subscribe:
    def __init__(self, title, period, price):
        self.title = title
        self.period = period
        self.price = price


class User:
    def __init__(self, tg_id, balance=0, total_buy=0, status=1, subscribe=False) -> None:
        self._tg_id = tg_id
        self._balance = balance
        self._total_buy = total_buy
        self.status = status
        self._subscribe = subscribe
        if self._subscribe:
            sub = get_subscribe(tg_id)
            self._subscribe_date = sub["date"]
            self._subscribe_period = sub["period"]

    @property
    def tg_id(self) -> int:
        return self._tg_id

    def replenish_balance(self, quantity) -> None:
        self._balance += quantity

    def buy(self, price, period) -> bool:
        if self._balance - price >= 0:
            self._balance = self._balance - price
            if not self._subscribe:
                self._subscribe = True
                self._subscribe_date = datetime.date.today()
                self._subscribe_period = round(30.4*period)
            else:
                self._subscribe_period += datetime.timedelta(round(30.4*period))
            self._total_buy += price
            return True
        return False


