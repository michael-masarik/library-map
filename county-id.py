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

def main(city,state):
    lat, lon = get_lat_lon(city, state)
    if lat is not None and lon is not None:
        fips = FIPS(lat, lon)
        data = { fips: library_name }
        print(f"FIPS code for {city}, {state} is: {fips}")
        print("Libary JSON data:")
        print(data)
        return data
        
    else:
        print("Could not find the location.")
main(city_input, state_input)
def check_file(filename, data):
    try:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
            # data is a dict: {fips: library}
            key, value = next(iter(data.items()))
            # Check if this pair already exists
            exists = any(entry["fips"] == key and entry["library"] == value for entry in existing_data)
            if exists:
                print("Data already exists in the file.")
            else:
                existing_data.append({"fips": key, "library": value})
                with open(filename, 'w') as file:
                    json.dump(existing_data, file, indent=4)
                print("Data added to the file.")
    except FileNotFoundError:
        key, value = next(iter(data.items()))
        with open(filename, 'w') as file:
            json.dump([{"fips": key, "library": value}], file, indent=4)
        print("File not found. Created a new file and added the data.")


