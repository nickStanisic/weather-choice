import requests 

def callApi(i,j,api_key,units):
    return requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={i}&lon={j}&appid={api_key}&units={units}')