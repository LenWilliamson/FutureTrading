# Convert unix time stamp to human readable format

import datetime as dt
from typing import Generator

from dateutil.relativedelta import relativedelta


def time_converter(time_stamp: float, blank: bool = False) -> str:
    """
    Gets posix time stamp in seconds and converts it to human readable format
    :param blank: Separation between day and hours is a blank space instead of underscore
    :param time_stamp: posix time in milliseconds
    :return: %Y-%m-%d_%H:%M:%S
    """
    if blank:
        date_time: str = dt.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        date_time: str = dt.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d_%H:%M:%S")
    return date_time


def date_time_generator(start: dt.datetime, end: dt.datetime, delta: dt.timedelta) -> Generator[dt.datetime, None, None]:
    """
    TODO Testen
    Creates a generator of datetime objects within start and end time separated by exactly delta.
    Note:   When you call a function that contains a yield statement anywhere, you get a generator object,
            but no code runs. Then each time you extract an object from the generator, Python executes code
            in the function until it comes to a yield statement, then pauses and delivers the object. When
            you extract another object, Python resumes just after the yield and continues until it reaches
            another yield (often the same one, but one iteration later). This continues until the function
            runs off the end, at which point the generator is deemed exhausted.
    :param start: start time stamp
    :param end: end time stamp
    :param delta: delta between generated datetime objects
    :return: Generator[dt.datetime, None, None]
    """
    curr: dt.datetime = start
    while curr < end:
        yield curr
        curr += delta
    yield end
