"""
Bank Account class
"""

from datetime import datetime

from time_zone import TimeZone


ts_id = {'id': 0}


class Account:
    """Account object"""

    _balance = 0
    _interest_rate = 0.005
    _first_name = None
    _last_name = None

    def __init__(self,
                 number: str,
                 first_name: str,
                 last_name: str,
                 zone: str = None) -> None:
        if zone is None:
            self.tz = TimeZone()
        else:
            self.tz = TimeZone(zone=zone)
        self.account_number = number
        self.first_name = first_name
        self.last_name = last_name
        self._full_name = None

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        if isinstance(first_name, str):
            self._first_name = first_name
            self._full_name = None
        else:
            raise ValueError('First name must be a string')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        if isinstance(last_name, str):
            self._last_name = last_name
            self._full_name = None
        else:
            raise ValueError('Last name must be a string')

    @property
    def full_name(self):
        if self._full_name is None:
            self._full_name = f'{self.first_name} {self.last_name}'
        return self._full_name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_balance: float) -> None:
        if new_balance >= 0:
            self._balance = new_balance
        else:
            raise ValueError('Not enough money on the account')

    @property
    def interest_rate(self):
        return self._interest_rate

    def generate_conf_number(self, code: str, dt: datetime) -> str:
        """Generate confirmation number for every transaction."""

        dt_stamp = dt.strftime('%Y%m%d%H%M%S')
        id_num = self.get_transaction_id()

        return f'{code}-{self.account_number}-{dt_stamp}-{id_num}'

    def deposit(self, amount: float) -> str:
        """Deposit amount on the balance."""

        self._balance += amount
        dt = datetime.now()

        return self.generate_conf_number('D', dt)

    def withdraw(self, amount: float) -> str:
        """Withdraw amount from the balance."""

        try:
            self.balance -= amount
            return self.generate_conf_number('W', datetime.now())
        except ValueError as err:
            print(err)
            return self.generate_conf_number('X', datetime.now())

    @staticmethod
    def get_transaction_id():
        """Get transaction id incrementing it by 1."""

        ts_id['id'] += 1
        return ts_id['id']
