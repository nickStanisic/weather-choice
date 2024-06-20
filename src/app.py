#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify
from weather import calculatePoints
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.sql import exists

load_dotenv()
api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(database_url, 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dt = db.Column(db.Integer, nullable = False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Weather {self.dt}>'

@app.before_request
def create_tables():
    db.create_all()



@app.route("/", methods=['GET','POST'])
def index():
    data = None
    
    fetch_weather_data()
    if request.method == 'POST':
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        startDate = request.form['startDate']
        endDate = request.form['endDate'] 
        data = calculatePoints(lowTemp, highTemp, startTime, endTime, startDate, endDate)
    return render_template('index.html', data=data)
    
@app.route('/weather', methods=['GET'])
def get_all_weather_data():
    weather_data = Weather.query.all()
    results = [
        {
            "dt": weather.dt,
            "lat": weather.lat,
            "lon": weather.lon,
            "temperature": weather.temperature
        } for weather in weather_data]
    return jsonify(results)


def fetch_weather_data():
    """Function to fetch weather data from an API and store it in the database."""
    min_lat = 41
    lat_increases = 3
    min_long = -108
    long_increases = 3
    units = "imperial"

    for i in range (min_lat,min_lat - lat_increases, -1):
        for j in range (min_long,min_long + long_increases):
            response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={i}&lon={j}&appid={api_key}&units={units}')
            if response.status_code == 200:
                data = response.json()
                for k in range (0,data.get('cnt')):
                    new_entry = Weather(dt=data.get('list')[k].get("dt"), 
                                        lat=i, 
                                        lon=j, 
                                        temperature=data.get('list')[k].get('main').get('temp'))
                    db.session.add(new_entry)
                    db.session.commit()
            else:
                print("Failed to fetch data")


if __name__ == '__main__':
    app.run(debug=True)