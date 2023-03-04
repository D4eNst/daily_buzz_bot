import datetime
import data.errors as e


class Subscribe:
    def __init__(self, sub_id=0, title=None, period=None, price=None):
        self.sub_id = sub_id
        self.title = title
        self.period = period
        self.price = price

    def get_values(self, form=1) -> tuple:
        if form == 1:
            return self.title, self.period, self.price
        elif form == 2:
            return self.sub_id, self.title, self.period, self.price


class User:
    def __init__(self, tg_id, balance=0, total_buy=0, status=1, sub=False, sub_date=None, sub_period=None) -> None:
        self._tg_id = tg_id
        self._balance = balance
        self._total_buy = total_buy
        self.status = status
        self._subscribe = sub
        self._subscribe_date = sub_date
        self._subscribe_period = sub_period

    @property
    def tg_id(self) -> int:
        return self._tg_id

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def subscribe(self) -> bool:
        return self._subscribe

    @property
    def subscribe_period(self) -> int:
        return self._subscribe_period

    @property
    def subscribe_date(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._subscribe_date, '%Y-%m-%d %H:%M:%S.%f')

    @property
    def subscribe_finish(self) -> datetime.datetime:
        finish_date = self.subscribe_date + datetime.timedelta(self.subscribe_period)
        return finish_date

    @property
    def subscribe_remains(self) -> int:
        return (self.subscribe_finish - datetime.datetime.today()).days + 1

    def replenish_balance(self, quantity) -> None:
        self._balance += quantity

    def buy_subscribe(self, price, period) -> None:
        if self._balance - price >= 0:
            self._balance = self._balance - price
            if not self._subscribe:
                self._subscribe = True
                self._subscribe_date = str(datetime.datetime.today())
                self._subscribe_period = round(30.4 * period)
            else:
                self._subscribe_period += datetime.timedelta(round(30.4 * period)).days
            self._total_buy += price
        else:
            raise e.InsufficientFundsError()

    def del_subscribe(self) -> None:
        self._subscribe = False
        self._subscribe_date = None
        self._subscribe_period = None

    def get_values(self, form=1) -> tuple:
        if form == 1:
            return self._balance, self._total_buy, self.status, \
                self._subscribe, self._subscribe_date, self._subscribe_period, self._tg_id
        elif form == 2:
            return self._tg_id, self._balance, self._total_buy, self.status, \
                self._subscribe, self._subscribe_date, self._subscribe_period

    def show(self) -> str:
        return f"{self._tg_id}\n" \
               f"{self._balance}\n" \
               f"{self._total_buy}\n" \
               f"{self.status}\n" \
               f"{self._subscribe}\n" \
               f"{self._subscribe_date}\n" \
               f"{self._subscribe_period}"
