######## import depedencies ########
import json
import sqlalchemy

import datetime
from datetime import date, timedelta

from flask import Flask, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
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

# app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api.v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"Please enter dates in 'YYYY-MM-DD' format"
    )
#########

#@app.route("/api/v1.0/precipitation")
def rain():
    """Return Dates and Temp from the last year."""
    results = session.query(measurement.date,  measurement.tobs).\
        filter(measurement.date <= "2016-01-01", measurement.date >= "2016-01-01").\
        all()

    #create the JSON objects
    precipitation_list = [results]

    return jsonify(precipitation_list)
#########

#@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(station.name, station.station, station.elevation).all()
    #create dictionary for JSON
    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)
#########

#/api/v1.0/tobs
def tobs():
    # Query temperatures
    """Return a list of tobs for the previous year"""
    results = session.query(station.name, measurement.date, measurement.tobs).\
        filter(measurement.date >= "2016-01-01", measurement.date <= "2017-01-01").\
        all()

    #create json, perhaps use dictionary
    tobs_list = []
    for result in results:
        row = {}
        row["Date"] = result[1]
        row["Station"] = result[0]
        row["Temperature"] = int(result[2])
        tobs_list.append(row)

    return jsonify(tobs_list)
#########

#/api/v1.0/<start>
def start(start):
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")

    delta = endDate - startDate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startDate + timedelta(days=i))
    
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)
  
    temp_avg = session.query(func.avg(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]
    temp_min = session.query(func.min(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]
    temp_max = session.query(func.max(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]

    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Average Temperature"] = temp_avg
    temp_dict["Minimum Temperature"] = temp_min
    temp_dict["Maximum Temperature"] = temp_max

    return jsonify(temp_dict)



#/api/v1.0/<start>/<end>
def startend(start, end):
   
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d")


    delta = endDate - startDate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startDate + timedelta(days=i))
    
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)
   
    temp_avg = session.query(func.avg(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]
    temp_min = session.query(func.min(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]
    temp_max = session.query(func.max(measurement.tobs))\
                .filter(measurement.date.in_(str_date_range))[0][0]

    temp_dict = {}
    temp_dict["Average Temperature"] = temp_avg
    temp_dict["Minimum Temperature"] = temp_min
    temp_dict["Maximum Temperature"] = temp_max

    return jsonify(temp_dict)




# # Getting a list of dates for the last 12 months
# base_date = datetime.strptime("2017-08-23", "%Y-%m-%d")
# numdays = 365
# date_list = [base_date - timedelta(days=x) for x in range(0, numdays)]

# # Converting them to a list of strings
# str_dates = []
# for date in date_list:
#     new_date = date.strftime("%Y-%m-%d")
#     str_dates.append(new_date)

