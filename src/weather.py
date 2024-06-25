from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
min_lat = 41
lat_increases = 5
min_long = -109
long_increases = 7

def get_temperatures_for_colorado(start, end, lowTemp, highTemp, json_data):
    colorado_temperature_list = []
    for i in range (min_lat,min_lat - lat_increases, -1):
        for j in range (min_long,min_long + long_increases):
            withinRange = True
            for k in range(start, end):
                currentTemp = json_data[k].get('temperature')
                if currentTemp < float(lowTemp) or currentTemp > float(highTemp):
                    withinRange = False
            colorado_temperature_list.append({'lat': i, 'lon': j, 'withinRange': withinRange})
            start = start + 40
            end = end + 40
    return colorado_temperature_list

def calculatePoints(lowTemp, highTemp, startTime, endTime, json_data):
    #range determined by date/time
    startIndex = 0
    while startTime >= json_data[startIndex].get('dt'):
        startIndex += 1
    endIndex = startIndex
    while endTime > json_data[endIndex].get('dt'):
        endIndex += 1
    return get_temperatures_for_colorado(startIndex,endIndex,lowTemp,highTemp, json_data)
