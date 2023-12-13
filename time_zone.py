import pytz
from datetime import datetime


class TimeZone:
    """Time zone information."""

    _name = None

    def __init__(self, zone: str):
        self.name = zone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, zone):
        if not isinstance(zone, str):
            raise ValueError('Timezone must be a string.')
        if len(str(zone).strip()) == 0:
            raise ValueError('Timezone name cannot be empty.')
        if zone not in pytz.all_timezones:
            raise ValueError('No such a timezone.')
        self._name = zone

    @property
    def offset(self):
        dt = datetime.now(tz=pytz.timezone(self.name))
        return dt.utcoffset()


if __name__ == '__main__':
    # tz = TimeZone('Asia/Jerusalem')
    tz = TimeZone('Asia/Jerusalem')
    dt_now = datetime.utcnow()
    print(dt_now)
    print(dt_now + tz.offset)
    # print(tz.localize(datetime.now()).strftime('%Z %z'))
    # print(tz.utcoffset(datetime.now()))
