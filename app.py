from flask import Flask, render_template
import os
import requests
app = Flask(__name__)

@app.route('/')
def index():

    #these are the parameters we have to set for search query to google places api
    #latitude and longitude of user inputted location, set manually to UCSD, later use 
    #geolocation api to change:
    location = "32.8801,-117.2340" 
    #radius set as default to 50000 meters, can change later to user input 
    radius = "50000"
    searchType = "restaurant"
    key = os.environ.get("API_KEY")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius="+radius+"&type="+searchType+"&key="+key
    
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #places stores the list of nearby places that google has retrieved
    places = []
    response_json = response.json()
    places.extend(response_json["results"])

    #what fields do we want to extract from the info google stores abt each place
    #so far thinking restaurant name, formatted address, opening hours

    rest_names = []
    rest_addresses = []
    rest_open = []

    for place in places:
        try:
            rest_names.append(place['name'])
        except: 
            rest_names.append('none')

        try: 
            rest_addresses.append(place['formatted_address'])
        except: 
            rest_addresses.append('none')

        try:
            rest_open.append(place['opening_hours'])
        except:
            rest_open.append('none')

    print(*rest_names, sep = ", ")
    return "hello world"

app.run(host='0.0.0.0', port=81)