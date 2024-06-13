#!/usr/bin/env python3

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    data = None
    lowTemp = 0
    highTemp = 0
    if request.method == 'POST':
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        startDate = request.form['startDate']
        endDate = request.form['endDate'] 
        data = "hello"
        #data = calculatePoints(lowTemp, highTemp, startTime, endTime, startDate, endDate)
    return render_template('index.html', data=data)