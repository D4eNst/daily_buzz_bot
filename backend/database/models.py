import datetime


def get_subscribe(tg_id):
    sub_start = datetime.date(2023, 1, 1)
    sub_period = 12
    return {
        "date": sub_start,
        "period": round(sub_period * 30.4)
    }


class Subscribe:
    def __init__(self, title, period, price):
        self.title = title
        self.period = period
        self.price = price


class User:
    def __init__(self, tg_id, balance=0, total_buy=0, status=1, sub=False, sub_date=None, sub_period=None) -> None:
        self._tg_id = tg_id
        self._balance = balance
        self._total_buy = total_buy
        self.status = status
        self._subscribe = sub
        self._subscribe_date = sub_date
        self._subscribe_period = sub_period
        if self._subscribe:
            subscribe = get_subscribe(tg_id)
            self._subscribe_date = subscribe["date"]
            self._subscribe_period = subscribe["period"]

    @property
    def tg_id(self) -> int:
        return self._tg_id

    @property
    def balance(self) -> int:
        return self._balance

    def replenish_balance(self, quantity) -> None:
        self._balance += quantity

    def buy(self, price, period) -> bool:
        if self._balance - price >= 0:
            self._balance = self._balance - price
            if not self._subscribe:
                self._subscribe = True
                self._subscribe_date = datetime.date.today()
                self._subscribe_period = round(30.4 * period)
            else:
                self._subscribe_period += datetime.timedelta(round(30.4 * period))
            self._total_buy += price
            return True
        return False

    def get_values(self) -> tuple:

        return self._balance, self._total_buy, self.status, \
            self._subscribe, self._subscribe_date, self._subscribe_period, self._tg_id

    def show(self) -> str:
        return f"{self._tg_id}\n" \
               f"{self._balance}\n" \
               f"{self._total_buy}\n" \
               f"{self.status}\n" \
               f"{self._subscribe}\n" \
               f"{self._subscribe_date}\n" \
               f"{self._subscribe_period}"
