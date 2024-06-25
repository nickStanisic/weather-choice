
def get_temperatures_for_colorado(min_lat, lat_increases, min_long, long_increases, start, end, lowTemp, highTemp, json_data):        
    colorado_temperature_list = []
    for i in range (min_lat,min_lat - lat_increases, -1):
        for j in range (min_long,min_long + long_increases):
            withinRange = True
            for k in range(start, end):
                withinRange = checkTemperature(json_data[k].get('temperature'), float(lowTemp), float(highTemp))
                if withinRange == False:
                    break
            colorado_temperature_list.append({'lat': i, 'lon': j, 'withinRange': withinRange})
            start += 40
            end += 40
    return colorado_temperature_list

def checkTemperature(currentTemp, lowTemp, highTemp):
    if currentTemp < lowTemp or currentTemp > highTemp:
        return False
    else:
        return True

def calculatePoints(min_lat, lat_increases, min_long, long_increases, lowTemp, highTemp, startTime, endTime, json_data):
    #range determined by date/time
    if startTime > endTime:
        return None
    startIndex = 0
    while startTime >= json_data[startIndex].get('dt'):
        startIndex += 1
    endIndex = startIndex
    while endTime > json_data[endIndex].get('dt'):
        endIndex += 1
    return get_temperatures_for_colorado(min_lat, lat_increases, min_long, long_increases, startIndex,endIndex,lowTemp,highTemp, json_data)
