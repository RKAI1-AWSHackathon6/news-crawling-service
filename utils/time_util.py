import datetime

def get_midday_from_epoch(epoch):
    if epoch is None:
        return epoch

    date_time = datetime.datetime.fromtimestamp(epoch)

    return int(datetime.datetime(date_time.year, date_time.month,date_time.day, 12, 0, 0).timestamp())

def get_start_day_from_epoch(epoch):
    if epoch is None:
        return epoch
        
    date_time = datetime.datetime.fromtimestamp(epoch)
    return int(datetime.datetime(date_time.year, date_time.month,date_time.day, 0, 0, 0).timestamp())

def get_now_time_stamp():
    return int(datetime.datetime.now().timestamp())

def get_diff_in_hours(datetimea, datetimeb):
    return (datetimea - datetimeb).total_seconds() / 3600

def get_diff_in_minutes(datetimea, datetimeb):
    return (datetimea - datetimeb).total_seconds() / 60

def to_timestamp(datetime):
    return int(datetime.timestamp())