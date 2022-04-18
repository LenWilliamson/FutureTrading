# Convert unix time stamp to human readable format

import datetime as dt


def time_converter(time_stamp: int, blank: bool = False) -> str:
    """
    Gets posix time stamp in milliseconds and converts it to human readable format
    :param blank: Separation between day and hours is a blank space instead of underscore
    :param time_stamp: posix time in milliseconds
    :return: %Y-%m-%d_%H:%M:%S
    """
    if blank:
        date_time: str = dt.datetime.fromtimestamp(time_stamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
    else:
        date_time: str = dt.datetime.fromtimestamp(time_stamp / 1000).strftime("%Y-%m-%d_%H:%M:%S")
    return date_time
