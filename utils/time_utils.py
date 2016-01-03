import iso8601
import datetime
import time
import pytz


def utcnow():
    return datetime.datetime.now(tz=pytz.utc).timetuple()


def to_utc(in_time_str):
    return iso8601.parse_date(in_time_str).utctimetuple()


def is_time_in_the_past(time_in):
    return to_utc(time_in) < utcnow()


def utcnow_str():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', utcnow())
