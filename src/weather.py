import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
min_lat = 41
lat_increases = 3
min_long = -108
long_increases = 3

def get_weather_data(lat, lon, API_key, units):
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units={units}').json()
    return resp

def get_temperatures_for_colorado(start, end, lowTemp, highTemp):
    colorado_temperature_list = []
    for i in range (min_lat,min_lat - lat_increases, -1):
        temps_for_lat = []
        for j in range (min_long,min_long + long_increases):
            data = get_weather_data(i,j,api_key,"imperial")
            withinRange = True
            for k in range(start, end):
                currentTemp = data.get('list')[k].get('main').get('temp')
                if currentTemp < float(int(lowTemp)) or currentTemp > float(int(highTemp)):
                    withinRange = False
            temps_for_lat.append(withinRange)
        colorado_temperature_list.append(temps_for_lat)
    return colorado_temperature_list

def calculatePoints(lowTemp, highTemp, startTime, endTime, startDate, endDate):
    #range determined by date/time
    start = int(startDate) + int(startTime)
    end = int(endTime) + int(endDate) + 1
    returnData = get_temperatures_for_colorado(start,end, lowTemp, highTemp)
    return returnData