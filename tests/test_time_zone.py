"""
Tests for time zone class
"""
from unittest import TestCase
from datetime import datetime, timedelta

import pytz
from time_zone import TimeZone


class TestTimeZone(TestCase):
    """Tests for TimeZone class."""

    def test_default_settings(self):
        """Test the default attributes of the TimeZone class."""

        zone_name = 'UTC'
        tz = TimeZone(zone_name)
        expected_offset = timedelta(hours=0, minutes=0, seconds=0)

        self.assertEqual(tz.name, zone_name)
        self.assertEqual(tz.offset, expected_offset)

    def test_change_timezone(self):
        """Test setting another timezone."""

        tz = TimeZone('Asia/Jerusalem')
        expected_offset = datetime.now(pytz.timezone(tz.name)).utcoffset()

        self.assertEqual(tz.offset, expected_offset)
