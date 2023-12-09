import pytz
from datetime import datetime


class TimeZone:
    """Time zone information."""

    _tz = pytz.utc

    def __init__(self, zone: str = None):
        if zone is not None:
            self.tz = zone

    @property
    def tz(self):
        return self._tz.zone

    @tz.setter
    def tz(self, zone):
        if zone not in pytz.all_timezones:
            raise ValueError('No such a time zone.')
        self._tz = pytz.timezone(zone)

    @property
    def offset(self):
        return self._tz.localize(datetime.now()).strftime('%z')


if __name__ == '__main__':
    # tz = TimeZone('Asia/Jerusalem')
    tz = pytz.timezone('Asia/Jerusalem')
    print(pytz.all_timezones)
    # print(tz.localize(datetime.now()).strftime('%Z %z'))
    # print(tz.utcoffset(datetime.now()))
