import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("TRAVEL_PAYOUT_API_TOKEN")
BASE_URL = "https://api.travelpayouts.com"

HEADERS = {
    "x-access-token": API_TOKEN
}

class flight_search:
    def city_lookup():
        response = requests.get(
            "https://api.travelpayouts.com/data/en/cities.json",
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        return response.json()