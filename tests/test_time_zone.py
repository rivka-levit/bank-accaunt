"""
Tests for time zone class
"""
from unittest import TestCase
from datetime import timedelta

from time_zone import TimeZone


class TestTimeZone(TestCase):
    """Tests for TimeZone class."""

    def test_create_timezone_success(self):
        """Test creating time zone successfully."""

        zone_name = 'UTC'
        tz = TimeZone(zone_name)
        expected_offset = timedelta(hours=0, minutes=0, seconds=0)

        self.assertEqual(tz.name, zone_name)
        self.assertEqual(tz.offset, expected_offset)

    def test_timezone_equal(self):
        """Test __eq__ method of TimeZone class."""

        tz1 = TimeZone('Asia/Jerusalem')
        tz2 = TimeZone('Asia/Jerusalem')

        self.assertEqual(tz1, tz2)

    def test_timezone_not_equal(self):
        """Test not equal time zones."""

        tz1 = TimeZone('Asia/Jerusalem')
        tz2 = TimeZone('America/Los_Angeles')

        self.assertNotEqual(tz1, tz2)
