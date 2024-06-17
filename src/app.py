#!/usr/bin/env python3

from flask import Flask, request, render_template
from src.weather import calculatePoints
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Weather.sqlite3'


# db = SQLAlchemy(app)
# class Weather(db.Model):
#     wid = db.Column(db.Integer, primary_key = True)
#     lat = db.Column(db.Float, nullable=False)
#     lon = db.Column(db.Float, nullable=False)
#     temperature = db.Column(db.Float, nullable=False)


@app.route("/", methods=['GET','POST'])
def index():
    data = None
    if request.method == 'POST':
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        startDate = request.form['startDate']
        endDate = request.form['endDate'] 
        data = calculatePoints(lowTemp, highTemp, startTime, endTime, startDate, endDate)
    return render_template('index.html', data=data)