"""
Tests for account.
"""

from unittest import TestCase
from unittest.mock import patch

from datetime import datetime
import pytz

from account import Account
from time_zone import TimeZone


class TestAccount(TestCase):
    """Test account class."""

    def setUp(self):
        self.account = Account(
            number='123456',
            first_name='Name',
            last_name='Surname',
            zone='Asia/Jerusalem'
        )

    def test_account_init(self):
        """Test account initialization."""

        self.assertEqual(self.account.account_number, '123456')
        self.assertEqual(self.account.first_name, 'Name')
        self.assertEqual(self.account.last_name, 'Surname')
        self.assertEqual(self.account.full_name, 'Name Surname')

        offset = TimeZone('Asia/Jerusalem').offset

        self.assertEqual(self.account.tz.offset, offset)
        self.assertEqual(self.account.balance, 0)
        self.assertEqual(self.account.interest_rate, 0.005)

    @patch('account.Account.get_transaction_id')
    def test_generate_confirmation_number(self, mocked_get_transaction_id):
        """Test generating confirmation number of transaction."""

        dt = datetime.now()
        mocked_get_transaction_id.return_value = 5
        payload = {
            'code': 'D',
            'dt': dt
        }

        confirmation = self.account.generate_conf_number(**payload)
        expected = (f'D-{self.account.account_number}-'
                    f'{dt.strftime('%Y%m%d%H%M%S')}-5')

        self.assertEqual(confirmation, expected)

    def test_deposit_on_account(self):
        """Test deposit amount on the account's balance."""

        current_balance = self.account.balance
        amount = 10.5

        self.account.deposit(amount)

        self.assertEqual(self.account.balance, current_balance + amount)

    def test_withdrawal_from_account_success(self):
        """Test withdrawal amount from the account's balance."""

        self.account.deposit(100)
        self.account.withdraw(50)

        self.assertEqual(self.account.balance, 50)

    def test_withdrawal_from_account_declined(self):
        """Test withdrawal declined."""

        self.account.deposit(50)
        confirmation = self.account.withdraw(100)
        ts_code = confirmation.split('-')[0]

        self.assertEqual(ts_code, 'X')

    def test_pay_interest_to_account(self):
        """Test pay interest to the account's balance.'"""

        self.account.deposit(100)

        expected = (self.account.interest_rate * self.account.balance +
                    self.account.balance)

        confirmation = self.account.pay_interest()
        ts_code = confirmation.split('-')[0]

        self.assertEqual(self.account.balance, expected)
        self.assertEqual(ts_code, 'I')

    def test_get_transaction_method(self):
        """Test the get_transaction method returns a valid transaction."""

        preferred_tz = pytz.timezone(self.account.tz.name)
        dt_format = '%Y-%m-%d %H:%M:%S (%Z)'

        confirmation = self.account.deposit(100)

        id_num = int(confirmation.split('-')[-1])
        dt = confirmation.split('-')[-2]
        y, m, d, h, mt, sec = map(
            int,
            [dt[:4], dt[4:6], dt[6:8], dt[8:10], dt[10:12], dt[12:]]
        )
        dt_obj = datetime(y, m, d, h, mt, sec, tzinfo=pytz.utc)

        expected_time_utc = dt_obj.strftime(dt_format)
        expected_time = dt_obj.astimezone(preferred_tz).strftime(dt_format)

        tsn = self.account.get_transaction(confirmation, self.account.tz.name)

        self.assertEqual(tsn.account_number, self.account.account_number)
        self.assertEqual(tsn.transaction_code, 'D')
        self.assertEqual(tsn.transaction_id, id_num)
        self.assertEqual(tsn.time, expected_time)
        self.assertEqual(tsn.time_utc, expected_time_utc)
