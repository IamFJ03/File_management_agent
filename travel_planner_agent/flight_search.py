import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("TRAVEL_PAYOUT_API_TOKEN")
BASE_URL = "https://api.travelpayouts.com"

HEADERS = {
    "x-access-token": API_TOKEN
}

class FlightSearch:
    def make_request(self, endpoint: str, params: dict | None = None):
        response = requests.get(
            BASE_URL + endpoint,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("success", True):
            raise Exception(result.get("error"))

        return result
    def city_lookup(self):
        response = requests.get(
            "https://api.travelpayouts.com/data/en/cities.json",
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def airport_lookup(self):
        response = requests.get(
        "https://api.travelpayouts.com/data/en/airports.json",
        headers=HEADERS,
        timeout=30
    )
        response.raise_for_status()

        return response.json()

    def airline_lookup(self):
        response = requests.get(
        "https://api.travelpayouts.com/data/en/airlines.json",
        headers=HEADERS,
        timeout=30
    )
        response.raise_for_status()

        return response.json()

    def search_direct_flights(
            self,
            origin,
    destination,
    depart_date,
    return_date=None,
    currency="INR"
    ):
        params = {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "currency": currency
        }

        if return_date:
            params["return_date"] = return_date

        return self.make_request(
            "/v1/prices/direct",
            params
        )
    def search_calender_prices(
            self,
            origin,
            destination,
            depart_date,
            calendar_type="departure_date",
            return_date=None,
            length=None,
            currency="INR"
        ):

        params = {
            "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "calendar_type": calendar_type,
        "currency": currency
        }

        if return_date:
            params["return_date"] = return_date

        if length:
            params["length"] = length

        return self.make_request(
            "/v1/prices/calendar",
            params
        )

    def search_monthly_prices(
            self,
            origin,
            destination,
            currency="INR"
        ):

        params = {
            "origin": origin,
            "destination": destination,
            "currency": currency
        }

        return self.make_request(
            "/v1/prices/monthly",
            params
        )

    def popular_destination(
            self,
            origin,
            currency = "INR"
        ):

        params = {
            "origin": origin,
            "currency": currency
        }

        return self.make_request(
            "/v1/city-directions",
            params
        )