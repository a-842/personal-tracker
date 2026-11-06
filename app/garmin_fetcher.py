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



def get_sleep(date):
    with GarminPersonalApiClient(access_token) as client:
        data = client.get_daily_sleep(date)
    start = datetime.datetime.fromtimestamp(data.get("sleepStartTimestampGMT")/1000)
    end = datetime.datetime.fromtimestamp(data.get("sleepEndTimestampGMT")/1000)
    
    return (start, end)

def handle(date):
    sleep_data = get_sleep(date)
    database.insert_activity(sleep_data[0], sleep_data[1], "sleep")
    database.commit()


if __name__ == "__main__":
    handle("2026-11-06")
    