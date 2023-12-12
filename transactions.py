"""
Classes for transactions.
"""
import pytz


class Transaction:
    """Transaction object."""

    def __init__(self, code, acc_num, dt, id_num, tz):
        self.account_number = acc_num
        self.transaction_code = code
        self.transaction_id = id_num
        self.tz = pytz.timezone(tz)
        self.dt = dt

    @property
    def time(self):
        dt_format = '%Y-%m-%d %H:%M:%S (%Z)'

        return self.dt.astimezone(self.tz).strftime(dt_format)

    @property
    def time_utc(self):
        dt_format = '%Y-%m-%d %H:%M:%S (%Z)'

        return self.dt.strftime(dt_format)
