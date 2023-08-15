import requests
from tabulate import tabulate
from datetime import datetime, timezone


def query_lux_express(trip_date, origin_stop, destination_stop, persons: int):
    """
    Performs the GraphQL query to LuxExpress API to get the routes between the stops

    date: date for the trip as YYYY-MM-DD
    origin_stop: Stop ID for the origin
    destination_stop: Stop ID for the destination
    persons: Number of persons travelling

    Returns a requests object containing JSON
    """
    url = 'https://luxexpress.eu/graphql'

    headers = {
        'authority': 'luxexpress.eu',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,et;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'cversion=always; cf_clearance=MI7cH8YtqK.hEvfCGls9HTBWlVqx8N4VSOBSnLF8pJg-1691775574-0-1-1402f380.60bec62.4303ac60-0.2.1691775574',
        'origin': 'https://luxexpress.eu',
        'platform': 'web-next',
        'pragma': 'no-cache',
        'referer': 'https://luxexpress.eu/tickets/search/?promocode=&departDate' + str(
            trip_date) + '&currency=EUR&fromBusStopId=' + str(origin_stop) + '&toBusStopId=' + str(
            destination_stop) + '&passengers=' + str(
            persons) + '&affiliateId=',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    data = {
        "variables": {
            "departureDate": trip_date,
            "originBusStopId": origin_stop,
            "destinationBusStopId": destination_stop,
            "currency": "CURRENCY.EUR",
            "lang": "et",
            "fareClasses": [{"Id": "BONUS_SCHEME_GROUP.ADULT", "Count": persons}],
            "promoCode": "",
            "isPartOfRoundtrip": False,
            "onlyActive": False
        },
        "query": "query ($departureDate: Date!, $originBusStopId: Int, $destinationBusStopId: Int, $lang: String, "
                 "$currency: String, $fareClasses: [SearchFareClassInput], $promoCode: String, $isPartOfRoundtrip: "
                 "Boolean, $onlyActive: Boolean) {\n  search(\n    departureDate: $departureDate\n    originBusStopId: "
                 "$originBusStopId\n    destinationBusStopId: $destinationBusStopId\n    lang: $lang\n    currency: "
                 "$currency\n    fareClasses: $fareClasses\n    promoCode: $promoCode\n    isPartOfRoundtrip: "
                 "$isPartOfRoundtrip\n    onlyActive: $onlyActive\n  ) {\n    JourneyId\n    "
                 "DepartureDateTimeTimeZone\n    ArrivalDateTimeTimeZone\n    DepartureDateTime\n    "
                 "ArrivalDateTime\n    PlannedDepartureDateTime\n    PlannedArrivalDateTime\n    Duration\n    "
                 "OriginStopName\n    OriginStopId\n    DestinationStopName\n    DestinationStopId\n    Currency\n   "
                 " AvailableRegularSeats\n    SoldLaterRegularSeats\n    RegularPrice\n    "
                 "AvailableBusinessClassSeats\n    SoldLaterBusinessClassSeats\n    BusinessClassPrice\n    "
                 "AvailableCampaignSeats\n    SoldLaterCampaignSeats\n    CampaignPrice\n    "
                 "AvailableBusinessCampaignSeats\n    SoldLaterBusinessCampaignSeats\n    BusinessCampaignPrice\n    "
                 "RegularBusPrice\n    BusinessBusPrice\n    IsForSale\n    NotForSaleReasonType\n    PriceClasses {"
                 "\n      PriceClassName\n      SeatClassCategory\n      NumberOfSeats\n      Price\n      "
                 "__typename\n    }\n    IsChangeable\n    IsRefundable\n    IsPetOnBus\n    "
                 "IsAllergicPassengerOnBus\n    IsWheelchairAreaAvailable\n    Legs {\n      OrderNumber\n      "
                 "BusCompanyName\n      BrandName\n      BrandShortName\n      LineIdentifier1 {\n        Name\n     "
                 "   Value\n        __typename\n      }\n      LineIdentifier2 {\n        Name\n        Value\n     "
                 "   __typename\n      }\n      LineIdentifier3 {\n        Name\n        Value\n        "
                 "__typename\n      }\n      AvailableEquipment {\n        EquipmentCode\n        EquipmentName\n    "
                 "    EquipmentType\n        __typename\n      }\n      Passengers {\n        UnitPrice\n        "
                 "BasicDiscountPrice\n        BasicDiscountName\n        FinalPrice\n        VatPercentage\n        "
                 "RequestedFareClass\n        SeatPricings {\n          FinalPrice\n          UnitPrice\n          "
                 "BasicDiscountPrice\n          VatPercentage\n          IsBusinessClass\n          IsCampaignPrice\n "
                 "         IsCampaignTicketChangeable\n          IsCampaignTicketRefundable\n          IsBusPrice\n    "
                 "      SeatClassCategory\n          SeatClassName\n          __typename\n        }\n        "
                 "__typename\n      }\n      __typename\n    }\n    SalesFees {\n      TotalBusinessClassSalesFee\n "
                 "     TotalRegularSalesFee\n      TotalCampaignSalesFee\n      TotalBusinessClassCampaignFee\n      "
                 "__typename\n    }\n    Notifications {\n      NotificationMessage\n      __typename\n    }\n    "
                 "__typename\n  }\n}"
    }

    result = requests.post(url, json=data, headers=headers)
    return result


def print_result(api_response):
    format_price = lambda price: f"{price}€" if price is not None else "N/A"
    format_time = lambda datetime_str: datetime_str.split('T')[1][:5]
    # format_duration = lambda time_str: time_str[:5]

    table_data = []

    for journey in api_response:
        available_regular_seats = journey["AvailableRegularSeats"]
        regular_price = format_price(journey["RegularPrice"])
        departure_datetime = format_time(journey["DepartureDateTime"])
        arrival_datetime = format_time(journey["ArrivalDateTime"])
        available_business_class_seats = journey.get("AvailableBusinessClassSeats", None)
        business_class_price = format_price(journey.get("BusinessClassPrice", None))
        is_for_sale = journey["IsForSale"]

        if is_for_sale:
            table_data.append([
                departure_datetime,
                arrival_datetime,
                available_regular_seats,
                regular_price,
                available_business_class_seats,
                business_class_price,
            ])

    print(tabulate(table_data, tablefmt="grid"))


def get_valid_input(prompt):
    """
    Find the stopID of a bus stop at a location
    """
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input


def find_stop_id(stop_name, stops_dict):
    stop_id = stops_dict.get(stop_name)
    if stop_id is None:
        raise ValueError(f"Stop '{stop_name}' not found.")
    return stop_id


def main():
    # List of most bigger stops on LuxExpress lines, compiled over time with... heuristics and stuff (manually)
    stops_dict = {
        "Tallinn": 17028,
        "Tartu": 17058,
        "Riga": 18859,
        "Riga Airport": 18860,
        "Pärnu": 8723,
        "Viljandi": 12661,
        "Võru": 10527,
        "Narva": 16404,
        "Kuresaare": 7800,
        "Haapsalu": 8533,
        "Vilnius": 18862,
        "Warsaw": 18925,
        "St. Petersburg": 18880,
        "Kaunas": 18921,
        "Helsinki": 21874,
        "Suwalki": 23752
    }

    start_bus_stop = get_valid_input("Input starting stop: ")
    destination_bus_stop = get_valid_input("Input destination: ")
    input_date = input("Input date as YYYY-MM-DD: ")
    no_of_persons = int(get_valid_input("Input number of travellers: "))

    show_all_options = ''
    if not input_date:
        show_all_options = input("Show all trips today? (Y/N) ").capitalize()
        input_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    origin = find_stop_id(start_bus_stop, stops_dict)
    destination = find_stop_id(destination_bus_stop, stops_dict)

    if show_all_options == 'Y':
        result = query_lux_express(input_date, origin, destination, no_of_persons)
    else:
        future_date = str(datetime.strptime(input_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).strftime("%Y-%m-%d"))
        result = query_lux_express(future_date, origin, destination, no_of_persons)

    if result.status_code == 200:
        response_json = result.json()
        search_results = response_json["data"]["search"]

        print(f"Trip: {start_bus_stop} --> {destination_bus_stop}\n")
        print_result(search_results)


if __name__ == "__main__":
    main()
