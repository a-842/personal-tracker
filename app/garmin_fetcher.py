import os 
from dotenv import load_dotenv
from garmin_personal_api import PersonalApiAuthenticator, GarminPersonalApiClient

load_dotenv()

api_key = os.getenv("GARMIN_PERSONAL_API_KEY")
if not api_key:
    raise ValueError("Garmin API key not found, add it in your .env file")

with PersonalApiAuthenticator() as authenticator:
        token_data = authenticator.obtain_token(api_key)
        access_token = token_data.access_token

with GarminPersonalApiClient(access_token) as client:
      heart_rate_zones = client.get_heart_rate_zones()
      print(heart_rate_zones)