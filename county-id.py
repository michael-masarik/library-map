# This script prodcuces a JSON object for the library-by-fips.json file
# It takes a city, state, and library as input, retrieves the latitude and longitude.
# Then all you have to do is check to see if the object is the library-by-fips.json file.
import requests
import json
city_input = input("Enter the city: ")
state_input = input("Enter the state: ")
library_name = input("Enter the library name: ")
def get_lat_lon(city, state):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&state={state}&format=json"
    headers = { 'User-Agent': 'Mozilla/5.0 (compatible; my-script/1.0)' }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            print(f"Lat: {data[0]['lat']}, Lon: {data[0]['lon']}")
            return data[0]['lat'], data[0]['lon']
        else:
            print(f"No results found for {city}, {state}. Full response: {data}")
    return None, None
def FIPS(lat,lon):
    url = f"https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lon}&format=json"
    response = requests.get(url)
    data = response.json()
    fips = data['County']['FIPS']
    print(f"FIPS code: {fips}")
    return fips
def check_file(filename, data):
    try:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
            # Check if this pair already exists
            exists = any(
                entry.get("fips") == data["fips"] and entry.get("library") == data["library"]
                for entry in existing_data
            )
            if exists:
                print("Data already exists in the file.")
            else:
                existing_data.append(data)
                with open(filename, 'w') as file:
                    json.dump(existing_data, file, indent=4)
                print("Data added to the file.")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)
        print("File not found. Created a new file and added the data.")

def main(city,state):
    lat, lon = get_lat_lon(city, state)
    if lat is not None and lon is not None:
        fips = FIPS(lat, lon)
        data = { "fips": fips, "library" : library_name }
        print(f"FIPS code for {city}, {state} is: {fips}")
        print("Libary JSON data:")
        print(data)
        if data:
            check_file('libraries-by-fips.json', data)
            print("Data has been checked and updated in the file.") 
        else:
            print("No data to write to the file.")
            return None
    else:
        print("Could not retrieve latitude and longitude for the given city and state.")
        return None
main(city_input, state_input)


