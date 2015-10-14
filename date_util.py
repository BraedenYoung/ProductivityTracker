import datetime
import time

from dateutil import tz


def get_time_delta(current, previous):
    return strfdelta((current - previous),
    '{minutes}') if previous else ''


def format_and_localize_time(time_value):
    time_value = time_value.replace(tzinfo=tz.tzutc())
    localized_time = time_value.astimezone(tz.tzlocal())

    return localized_time.strftime("%Y-%m-%d %H:%M:%S")


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
