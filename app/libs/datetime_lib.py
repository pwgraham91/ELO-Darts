import pytz
import tzlocal


def convert_to_local_from_utc(utc_time):
    local_timezone = tzlocal.get_localzone()
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time


def convert_to_tz_from_utc(utc_time, tz):
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(tz))
    return local_time
