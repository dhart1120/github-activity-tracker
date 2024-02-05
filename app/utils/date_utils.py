from datetime import datetime
import pytz

def convert_to_local(datetime_str: datetime, timezone = "America/Chicago"):
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.utc)
    datetime_obj_local = datetime_obj_utc.astimezone(pytz.timezone(timezone))
    return datetime_obj_local.strftime("%B %d, %Y, %I:%M:%S %p %Z") # February 01, 2024, 04:03:28 AM CST

