# Author: Joel Ruuben Seene
"""
Project idea: Query train times from Elron (Estonian National Passenger Rail Provider)
Ask starting stop and destination stop, date --> Check the list of stops for stop id (internal code)
    If the stop doesn't exist, notify the user

Make query against the API for schedule
Filter out necessary data
present as table in console


Possible further development --> do the same for LuxExpress site
Necessity with Lux --> Check for existing stop, translate to code, create URL, make query, etc

Show both side-by-side --> Elron | LuxExpress (if applicable)
"""

import json
from datetime import date, datetime, timezone, timedelta

import requests
from tabulate import tabulate


def stop_id(stop_location):
    try:
        a = stop_location.strip()
        b = a.capitalize()

        with open("Stops.json", encoding="utf8") as f:
            data = json.load(f)
            for stops in data:
                if stops["stop_name"] == b:
                    return stops["stop_area_id"]

    except TypeError as e:
        print("Incorrect input")


def api_query(origin_stop_id, destination_stop_id, date):
    """
    Queries the Ridango API for the train times between 2 stops

    :param origin_stop_id: Origin Stop ID
    :param destination_stop_id: Destination stop ID
    :param date: Trip date
    :return: API response in JSON

    Original code generated with Postman, modified to fit the project
    """

    url = "https://api.ridango.com/v2/64/intercity/stopareas/trips/direct"

    payload = json.dumps({
        "date": str(date),
        "origin_stop_area_id": str(origin_stop_id),
        "destination_stop_area_id": str(destination_stop_id),
        "channel": "web"
    })

    headers = {
        'authority': 'api.ridango.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,et;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://elron.pilet.ee',
        'pragma': 'no-cache',
        'referer': 'https://elron.pilet.ee/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.request("PUT", url, headers=headers, data=payload).json()

    return response


def get_trip_info(response: json, output: list, time=None):
    """
    Function to process the API response

    :param response: Response from the API in JSON
    :param output: List of the times and prices
    :param time: "Current time" if specified
    :return:
    """
    for journey in response["journeys"]:
        for trip in journey["trips"]:
            arrival_time = datetime.fromisoformat(trip["arrival_time"]) \
                .replace(tzinfo=timezone(offset=timedelta()))  # Needed for comparison, timezone def
            departure_time = datetime.fromisoformat(trip["departure_time"]) \
                .replace(tzinfo=timezone(offset=timedelta()))  # Needed for comparison, timezone def

            price = str(trip["product"]["price"]) + '\u20AC'  # Get the price info, add '€' as unicode

            if time and time < departure_time:  # If a time to compare to has been supplied
                formatted_departure = datetime.strftime(departure_time, '%H:%M') \
                                      + ' - ' \
                                      + datetime.strftime(arrival_time, '%H:%M')
                departure = [formatted_departure, price]

            else:  # Show all, since no time to start from has been given
                formatted_departure = datetime.strftime(departure_time, '%H:%M') \
                                      + ' - ' \
                                      + datetime.strftime(arrival_time, '%H:%M')
                departure = [formatted_departure, price]

            output.append(departure)

    return output


if __name__ == '__main__':

    origin = input("Input starting stop: ")
    destination = input("Input destination: ")
    input_date = input("Input date as YYYY-MM-DD (leave empty for today): ")

    if input_date == '':  # If the input is empty, add current date (YYYY-MM-DD)
        input_date = str(date.today())

    origin_id = stop_id(origin)  # "64-5924-93"
    destination_id = stop_id(destination)  # "64-5924-97"

    api_response = api_query(origin_id, destination_id, input_date)
    result = []
    current_time = datetime.now().replace(tzinfo=timezone(offset=timedelta()))

    get_trip_info(api_response, result)

    print(f"\n{origin} --> {destination}")
    print(tabulate(result, tablefmt="grid"))
