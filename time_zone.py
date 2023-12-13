import pytz
from datetime import datetime


class TimeZone:
    """Time zone information."""

    _name = None
    _offset_hours = None
    _offset_minutes = None

    def __init__(self, zone: str):
        self.name = zone
        self._offset = self.offset

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
        offset = dt.strftime('%z')
        self._offset_hours = int(offset[:3])
        self._offset_minutes = int(offset[0] + offset[3:])
        return dt.utcoffset()

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and
                self.name == other.name and
                self._offset_hours == other._offset_hours and
                self._offset_minutes == other._offset_minutes)

    def __repr__(self):
        return (f'TimeZone(name={self.name}, '
                f'offset_hours={self._offset_hours}, '
                f'offset_minutes={self._offset_minutes})')


if __name__ == '__main__':
    # tz = TimeZone('Asia/Jerusalem')
    tz = TimeZone('America/Los_Angeles')
    print(tz)
    # dt_now = datetime.utcnow()
    # print(dt_now)
    # print(tz.offset)
    # print(dt_now + tz.offset)
    # print(tz.localize(datetime.now()).strftime('%Z %z'))
    # print(tz.utcoffset(datetime.now()))
