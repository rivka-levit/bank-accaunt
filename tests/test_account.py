"""
Tests for account.
"""

from unittest import TestCase

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

    def test_generate_confirmation_number(self):
        """Test generating confirmation number of transaction."""

        dt = datetime.now()
        payload = {
            'code': 'D',
            'dt': dt
        }

        confirmation = self.account.generate_conf_number(**payload)
        expected = (f'D-{self.account.account_number}-'
                    f'{dt.strftime('%Y%m%d%H%M%S')}-1')

        self.assertEqual(confirmation, expected)
