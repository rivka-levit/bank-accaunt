"""
Tests for account.
"""

from unittest import TestCase
from unittest.mock import patch

from datetime import datetime

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
    def test_generate_confirmation_number(self, mocked_id):
        """Test generating confirmation number of transaction."""

        dt = datetime.now()
        mocked_id.return_value = 5
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
