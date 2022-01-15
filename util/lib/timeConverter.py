# Convert unix time stamp to human readable format

import datetime as dt


def time_converter(time_stamp: int):
    """
    Gets posix time stamp in milliseconds and converts it to human readable format
    :param time_stamp: posix time in milliseconds
    :return: %Y-%m-%d %H:%M:%S
    """
    date_time = dt.datetime.fromtimestamp(time_stamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
    return date_time
