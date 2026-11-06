from app import database
import datetime

def get_timeline_data(date):
    raw_data = database.get_date_activities(date)

    out_data = []
    for activity in raw_data:
        start_seconds = (activity[0] - datetime.datetime.combine(date, datetime.time.min)).total_seconds()
        duration_seconds = max((activity[1] - activity[0]).total_seconds(), 60)

        left_percent = (start_seconds / 86400) * 100
        width_percent = (duration_seconds / 86400) * 100

        out_data.append((left_percent, width_percent, activity[2]))

    return out_data



        


    