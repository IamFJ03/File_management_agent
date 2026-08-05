import requests
import os

API_KEY = os.getenv("RAIL_RADAR_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

class TrainSearch:
    def train_lookup(self, train_name: str):
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

    def station_lookup(self, station_name:str):
        response = requests.get(
            "https://api.railradar.in/v1/lookup/stations",
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()
        stations = response.json()["data"]
        station_Code = None

        for code, name in stations.items():
            if station_name.lower() in name.lower():
                station_Code = code
                return station_Code

        return {
            "success": False,
            "message": f"No station found matching '{station_name}'."
        }

    def get_train_details(self, train_number: str, halts_only: bool = True):
        response = requests.get(
            f"https://api.railradar.in/v1/trains/{train_number}",
            params={"haltsOnly": str(halts_only).lower()},
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()["data"]

        train = data["train"]
        print(data["route"])
        route = [
        {
            "station_name": stop["station"]["name"],
            "arrival": stop.get("arrival"),
            "departure": stop.get("departure"),
            "platform": stop.get("platform")
        }
        for stop in data["route"]
    ]
        return {
        "train_number": train["number"],
        "train_name": train["name"],
        "source": train["source"]["name"],
        "destination": train["destination"]["name"],
        "category": train["category"],
        "run_days": train["runDays"],
        "route": route
        }

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
        
        data = response.json()["data"]
        print(data["route"])
        route = [
    {
        "station_name": stop["stationName"],
        "scheduled_arrival": stop.get("scheduledArrival"),
        "actual_arrival": stop.get("actualArrival"),
        "scheduled_departure": stop.get("scheduledDeparture"),
        "actual_departure": stop.get("actualDeparture"),
        "delay_arrival": stop.get("delayArrival"),
        "delay_departure": stop.get("delayDeparture"),
        "platform": stop.get("platform"),
        "status": stop.get("status")
    }
    for stop in data["route"]
]

        exceptions = [
    {
        "type": exc["type"],
        "message": exc["message"]
    }
    for exc in data.get("exceptions", [])
]
        previous_halt = data.get("previousHalt", {})
        next_halt = data.get("nextHalt", {})
        return {
        "train_number": data["trainNumber"],
        "train_name": data["trainName"],
        "journey_date": data["startDate"],
        "status": data["status"],
        "delay_minutes": data["delayMinutes"],
        "current_location": {
            "station_code": data["currentLocation"]["stationCode"],
            "status": data["currentLocation"]["status"]
        },
        "previous_halt": data["previousHalt"] if previous_halt else None,
        "next_halt": data["nextHalt"] if next_halt else None,
        "exceptions": exceptions,
        "route": route,
        "is_live": data.get("isLive")
    }

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
        data = response.json()["data"]

        trains = [
            {
                 "train_number": train["train"]["number"],
            "train_name": train["train"]["name"],
            "train_type": train["train"]["type"],
            "run_days": train["train"]["runDays"],
            "departure": train["from"]["departure"],
            "arrival": train["to"]["arrival"],
            "distance_km": train["distance"],
            "duration_minutes": train["duration"],
            "total_halts": train["totalHaltsBetween"]
            }
            for train in data["trains"]
        ]

        return {
            "source": data["from"]["name"],
        "destination": data["to"]["name"],
        "date": date,
        "total_trains": data["count"],
        "trains": trains
        }