import os
import requests


def get_restaurants(location):
    # these are the parameters we have to set for search query to google places api
    # latitude and longitude of user inputted location, set manually to UCSD, later use
    # geolocation api to change:
    # loc = "32.8801,-117.2340"
    # radius set as default to 50000 meters, can change later to user input
    radius = "50000"
    searchType = "restaurant"
    key = os.environ.get("GOOGLE_API_KEY")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + \
        "32.8801,-117.2340"+"&radius="+radius+"&type="+searchType+"&key="+key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # places stores the list of nearby places that google has retrieved
    places = []
    response_json = response.json()
    places.extend(response_json["results"])

    return places


def get_rest_names(restaurants):
    """ Get a list of the names of the restaurants. """
    rest_names = []
    for rest in restaurants:
        try:
            rest_names.append(restaurants['name'])
        except:
            rest_names.append('none')

    return rest_names


def get_rest_addresses(restaurants):
    """ Get a list of the addresses of the restaurants. """
    rest_addresses = []
    for rest in restaurants:
        try:
            rest_addresses.append(rest['formatted_address'])
        except:
            rest_addresses.append('none')
    return rest_addresses


def get_rest_hours(restaurants):
    """ Get the restaurant hours. """
    rest_hours = []
    for rest in restaurants:
        try:
            rest_hours.append(rest['opening_hours'])
        except:
            rest_hours.append('none')
    return rest_hours


print(get_rest_names(get_restaurants(("32.8801,-117.2340"))))
