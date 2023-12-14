"""
Bank Account class
"""

from datetime import datetime

import pytz
import itertools

from time_zone import TimeZone
from transactions import Transaction

transactions = dict()


class Account:
    """Account object"""

    transaction_counter = itertools.count(1)
    _tz = TimeZone('UTC')

    def __init__(self,
                 number: str,
                 first_name: str,
                 last_name: str,
                 zone: str = None) -> None:

        self.tz = TimeZone(zone=zone)
        self._account_number = number
        self._first_name = None
        self._last_name = None
        self.first_name = first_name
        self.last_name = last_name
        self._full_name = None
        self._balance = 0
        self._interest_rate = 0.005

    @property
    def account_number(self):
        return self._account_number

    @property
    def tz(self):
        return self._tz

    @tz.setter
    def tz(self, time_zone: TimeZone) -> None:
        if not isinstance(time_zone, TimeZone):
            raise ValueError('Time Zone must be a valid TimeZone object.')
        self._tz = time_zone

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, name: str) -> None:
        self._first_name = Account.validate_name(name, 'first name')
        self._full_name = None

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, name: str) -> None:
        self._last_name = Account.validate_name(name, 'last name')
        self._full_name = None

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
        id_num = next(Account.transaction_counter)
        transactions[id_num] = {
            'id_num': id_num,
            'code': code,
            'acc_num': self.account_number,
            'dt': dt
        }

        return f'{code}-{self.account_number}-{dt_stamp}-{id_num}'

    def deposit(self, amount: float) -> str:
        """Deposit amount on the balance."""

        self._balance += amount
        dt = datetime.now(tz=pytz.utc)

        return self.generate_conf_number('D', dt)

    def withdraw(self, amount: float) -> str:
        """Withdraw amount from the balance."""

        try:
            self.balance -= amount
            return self.generate_conf_number('W', datetime.now(tz=pytz.utc))
        except ValueError:
            return self.generate_conf_number('X', datetime.now(tz=pytz.utc))

    def pay_interest(self):
        """Deposit interest on the balance."""

        interest = self.balance * self.interest_rate
        self.deposit(interest)

        return self.generate_conf_number('I', datetime.now())

    @staticmethod
    def get_transaction(confirmation: str, tz: str) -> Transaction:
        """Return transaction by confirmation number."""

        id_num = int(confirmation.split('-')[-1])

        return Transaction(**transactions[id_num], tz=tz)

    @staticmethod
    def validate_name(value: str, field_name: str) -> str:
        """Validate the first name and the last name of the account holder."""

        if not isinstance(value, str):
            raise ValueError(
                f'{field_name.capitalize()} must be a string'
            )
        if len(value.strip()) == 0:
            raise ValueError(
                f'{field_name.capitalize()} can not be empty string.'
            )

        return value.strip()
