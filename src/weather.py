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
    return requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units={units}').json()

def get_temperatures_for_colorado(start, end, lowTemp, highTemp):
    colorado_temperature_list = []
    for i in range (min_lat,min_lat - lat_increases, -1):
        temps_for_lat = []
        for j in range (min_long,min_long + long_increases):
            withinRange = True
            for k in range(start, end):
                currentTemp = 0 #need to update this to assess db values
                if currentTemp < float(lowTemp) or currentTemp > float(highTemp):
                    withinRange = False
            temps_for_lat.append(withinRange)
        colorado_temperature_list.append(temps_for_lat)
    return colorado_temperature_list

def calculatePoints(lowTemp, highTemp, startTime, endTime, startDate, endDate):
    #range determined by date/time
    start = int(startDate) + int(startTime)
    end = int(endTime) + int(endDate) + 1
    return get_temperatures_for_colorado(start,end,lowTemp,highTemp)
