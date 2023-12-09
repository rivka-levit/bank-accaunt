"""
Tests for time zone class
"""
from unittest import TestCase
from datetime import datetime

import pytz
from time_zone import TimeZone


class TestTimeZone(TestCase):
    """Tests for TimeZone class."""

    def setUp(self):
        self.time_zone = TimeZone()

    def test_default_settings(self):
        """Test the default attributes of the TimeZone class."""

        self.assertEqual(self.time_zone.tz, pytz.utc.zone)
        self.assertEqual(self.time_zone.offset, '+0000')

    def test_change_timezone(self):
        """Test setting another timezone."""

        self.time_zone.tz = 'Asia/Jerusalem'
        expected_offset = (pytz.timezone('Asia/Jerusalem').
                           localize(datetime.now()).
                           strftime('%z'))
        self.assertEqual(self.time_zone.offset, expected_offset)
