######## import depedencies ########
import json
import sqlalchemy

import datetime
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label

import climatefunc
#################################################

app = Flask(__name__)

#################################################
# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)
#################################################

# Getting a list of dates for the last 12 months
base_date = datetime.strptime("2017-08-23", "%Y-%m-%d")
numdays = 365
date_list = [base_date - timedelta(days=x) for x in range(0, numdays)]

# Converting them to a list of strings
str_dates = []
for date in date_list:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)



@app.route("/")
def home():
    data = climatefunc.home()
    return(data)

@app.route("/api/v1.0/precipitation")
def precipitation():
    data = climatefunc.rain()
    return(data)

@app.route("/api/v1.0/stations")
def stations():
    data=climatefunc.stations()
    return(data)

@app.route("/api/v1.0/tobs")
def tobs():
    data=climatefunc.tobs()
    return(data)

@app.route("/api/v1.0/<start>")
def start(start):
    data=climatefunc.start(start)
    return(data)

@app.route("/api/v1.0/<start_date>/<end_date>/")
def startend(start,end):
    data=climatefunc.startend(start,end)
    return(data)

if __name__ == '__main__':
    app.run(debug=False)


# 2016-01-01