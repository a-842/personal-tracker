import os 
from dotenv import load_dotenv
from garmin_personal_api import PersonalApiAuthenticator, GarminPersonalApiClient
import datetime
from app import database

load_dotenv()

api_key = os.getenv("GARMIN_PERSONAL_API_KEY")
if not api_key:
    raise ValueError("Garmin API key not found, add it in your .env file")

with PersonalApiAuthenticator() as authenticator:
        token_data = authenticator.obtain_token(api_key)
        access_token = token_data.access_token



def sleep_timeline(date):
    with GarminPersonalApiClient(access_token) as client:
        data = client.get_daily_sleep(date)
    start = datetime.datetime.fromtimestamp(data.get("sleepStartTimestampGMT")/1000)
    end = datetime.datetime.fromtimestamp(data.get("sleepEndTimestampGMT")/1000)
    
    return (start, end)

def workouts_timeline(date):
    with GarminPersonalApiClient(access_token) as client:
        data = client.search_activities(start_date=date, end_date=date)
    
    formatted_data = []
    for activity in data:
        start = activity.get("startTimeGMT")
        end = activity.get("endTimeGMT")
        activity_type = activity.get("activityType", {}).get("typeKey")
        formatted_data.append((start, end, activity_type))

    return formatted_data
            
    

def handle(date):
    sleep_data = sleep_timeline(date)
    database.insert_activity(sleep_data[0], sleep_data[1], "sleeping")

    workout_data = workouts_timeline(date)
    for activity in workout_data:
        database.insert_activity(activity[0], activity[1], activity[2])

    database.commit()


if __name__ == "__main__":
    #workouts_timeline("2026-11-07")
    handle("2026-11-05")
    