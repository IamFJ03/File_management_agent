import requests
import os

API_KEY = os.getenv("RAIL_RADAR_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

class TrainSearch:
    def get_train_identifier(self, train_name: str):
        lookup = requests.get(
            "https://api.railradar.in/v1/lookup/trains",
            headers=HEADERS,
            timeout=20
        )
        lookup.raise_for_status()
        trains = lookup.json()["data"]
        train_number = None

        for number,name in trains.items():
            if train_name.lower() in name.lower():
                train_number = number

                return train_number

        
        return {
            "success": False,
            "message": f"No train found matching '{train_name}'."
            }


    def get_train_details(self, train_number: str, halts_only: bool = True):
        response = requests.get(
            f"https://api.railradar.in/v1/trains/{train_number}",
            params={"haltsOnly": str(halts_only).lower()},
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def get_train_status(self, train_number: str,journey_date: str, halts_only: bool = True):
        params = {
            "haltsOnly": str(halts_only).lower()
        }

        if journey_date:
            params["date"] = journey_date
        response = requests.get(
            f"https://api.railradar.in/v1/trains/{train_number}/live",
            params=params,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def get_trains_by_date(self, source: str, destination: str, date: str, live: bool = True, byCity: bool = True):

        params={
                "live": str(live).lower(),
                "byCity": str(byCity).lower()
                }
        if date:
            params["date"] = date

        response = requests.get(
            f"https://api.railradar.in/v1/trains/between/{source}/{destination}",
            params=params,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        return response.json()