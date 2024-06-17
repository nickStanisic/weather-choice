
# import requests
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# import os
# from app import db, Weather

# load_dotenv()
# api_key = os.getenv('API_KEY')
# min_lat = 41
# lat_increases = 3
# min_long = -108
# long_increases = 3


# def get_weather_data(lat, lon, API_key, units):
#     return requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units={units}').json()

# def populate_database():
#     lat = 41
#     lon = -108
#     units = "imperial"
#     data = get_weather_data(lat,lon,api_key,units)
#     for i in range (0,data.get('cnt')):
#         new_entry = Weather(wid=i,lat=lat,lon=lon,temperature=data.get('list')[i].get('main').get('temp'))
#         db.session.add(new_entry)
#         db.session.commit()