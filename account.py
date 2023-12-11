"""
Bank Account class
"""

from time_zone import TimeZone


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