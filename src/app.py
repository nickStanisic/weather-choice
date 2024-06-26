#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify, url_for
from src.dataAnalyzer.weather import calculatePoints
from src.form import DateTimeForm, generate_choices, generate_time_choices
from src.map import create_map
from flask_sqlalchemy import SQLAlchemy
from src.dataCollector.callApi import callApi
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_migrate import Migrate


load_dotenv()
api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URI')
min_lat = 41
lat_increases = 5
min_long = -109
long_increases = 7
units = "imperial"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uav30uida8mg8g:p383a3af79ed9fde44f7ff64877846d194765dfde87defe46fa15581999267d6e@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d71dlt6vcpgav8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    now = datetime.now()
    time = datetime.timestamp(now)

    if Weather.query.count() == 0:
        fetch_weather_data()
    else:
        first_weather = Weather.query.first()
        if first_weather:
            timestamp = first_weather.dt
            if timestamp + 10800 < time:
                db.session.query(Weather).delete()
                db.session.commit()
                fetch_weather_data()

    form = DateTimeForm(request.form)
    form.endDate.choices = generate_choices()
    form.endTime.choices = generate_time_choices()
    form.startDate.choices = generate_choices()
    form.startTime.choices = generate_time_choices()

    if request.method == "GET":
        return render_template('index.html', form=form)

    if request.method == 'POST':
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        startTime = form.startTime.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        endTime = form.endTime.data
        endTimeStamp = datetime.strptime(f'{endDate} {endTime}', '%Y-%m-%d %H:%M').timestamp()
        startTimeStamp = datetime.strptime(f'{startDate} {startTime}', '%Y-%m-%d %H:%M').timestamp()
        data = calculatePoints(min_lat, lat_increases, min_long, long_increases, lowTemp, highTemp, startTimeStamp, endTimeStamp, get_all_weather_data())
        map_path = create_map(lowTemp, highTemp, data)
        return render_template('index.html', data=data, form=form, map_url=url_for('static', filename='map.png'), map_path=map_path)
    
@app.route('/weather', methods=['GET'])
def get_weather_data():
    return jsonify(get_all_weather_data())
    
@app.route('/health', methods=['GET'])
def healthCheck():
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

def fetch_weather_data():
    """Function to fetch weather data from an API and store it in the database."""
    for i in range (min_lat,min_lat - lat_increases, -1):
        for j in range (min_long,min_long + long_increases, 1):
            response = callApi(i,j,api_key,units)
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

def get_all_weather_data():
    weather_data = Weather.query.all()
    results = [
        {
            "dt": weather.dt,
            "lat": weather.lat,
            "lon": weather.lon,
            "temperature": weather.temperature
        } for weather in weather_data]
    print(results)
    return results


if __name__ == '__main__':
    app.run(debug=True)