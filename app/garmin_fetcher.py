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
    
    return (start, end, "sleeping")

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

def moveIQ_timeline(date):
    with GarminPersonalApiClient(access_token) as client:
        data = client.get_daily_summaries(start_date=date, end_date=date)

    events = data.get("data", [])[0].get("bodyBattery", {}).get("activityEvents", [])

    moveIQ_blocks = []
    for event in events:
        event_type = event.get("eventType")
        if event_type != "SLEEP":
            start = datetime.datetime.strptime(event.get("eventStartTimeGmt").split(".")[0], "%Y-%m-%dT%H:%M:%S")
            end = start + datetime.timedelta(milliseconds=event.get("durationInMillis", 0))
            moveIQ_blocks.append((start, end, f"MoveIQ: {event_type} - {event.get("shortFeedback")}"))
    return moveIQ_blocks
    

def handle(date):
    sleep_data = sleep_timeline(date)
    database.insert_activity(sleep_data[0], sleep_data[1], sleep_data[2])

    workout_data = workouts_timeline(date)
    for activity in workout_data:
        database.insert_activity(activity[0], activity[1], activity[2])

    moveIQ_data = moveIQ_timeline(date)
    for activity in moveIQ_data:
        database.insert_activity(activity[0], activity[1], activity[2])

    database.commit()


if __name__ == "__main__":
    database.setup()
    #print(moveIQ_timeline("2026-11-05"))
    handle("2026-11-06")
    database.close()
    