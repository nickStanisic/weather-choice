from wtforms import Form, SelectField
from datetime import datetime, timedelta

class DateTimeForm(Form):
    startDate = SelectField('Date', choices=[])
    startTime = SelectField('Time', choices=[])
    endDate = SelectField('Date', choices=[])
    endTime = SelectField('Time', choices=[])

def generate_choices():
    today = datetime.today()
    choices = [(today + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(4)]
    return [(date, date) for date in choices]

def generate_time_choices():
    times = [(datetime.strptime(f'{hour}:{minute:02d}', '%H:%M')).strftime('%H:%M') for hour in range(24) for minute in (0,30)]
    return [(time,time) for time in times]