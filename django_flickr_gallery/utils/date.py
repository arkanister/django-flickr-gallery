import time
import datetime


def parse_unix_datetime(str_value):
    if isinstance(str_value, (str, bytes)):
        str_value = int(str_value)

    time_struct = time.localtime(int(str_value))
    return datetime.datetime(
        year=time_struct.tm_year,
        month=time_struct.tm_mon,
        day=time_struct.tm_mday,
        hour=time_struct.tm_hour,
        minute=time_struct.tm_min,
        second=time_struct.tm_sec)
