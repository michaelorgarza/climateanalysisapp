
# coding: utf-8

# # 11-Advanced-Data-Storage-and-Retrieval/HOMEWORK/ClimateApp

# In[38]:


from flask import Flask, jsonify, send_file
from datetime import datetime, timedelta
import json

# ### Python SQL toolkit

# In[39]:


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label


# ### Construct Database

# In[40]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)


# ### Construct Routes 

# In[41]:


app = Flask(__name__)
# home route
@app.route("/")
def home():
    return (
        f"<bold>Welcome! Welcome! Welcome... to the Hawaii Weather Data API!<br/>"
        f"<bold>Available Routes:<br/><br/></bold>"
        f"<bold>General data:<br/><br/></bold>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"<bold>Specific trip data:<br/><br/></bold>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/"
        )
        


# In[42]:


def rain_range(start_date, end_date):
    start = start_date - timedelta(days=365)
    end = end_date - timedelta(days=365)
    
    temp_values = session.query(label('max_prcp',func.max(measurement.prcp)),\
                    label('min_prcp',func.min(measurement.prcp)),\
                    label('avg_prcp',func.avg(measurement.prcp))).\
                    filter(measurement.date >= start).\
                    filter(measurement.date <= end)
    
@app.route("/api/v1.0/precipitation")
def rain_json():
    results = rain_range(measurement.prcp)
    return jsonify(results)


# In[43]:


@app.route("/api/v1.0/stations")
def stations():
    stations_list = []
    act_stations = session.query(station.station, func.count(station.station))
    for station in act_stations:
        station_dict = {"id": station[0], "name": station[1], "latitude": station[2], "longitude": station[3], "elevation": station[4]}
        stations_list.append(station_dict)
    return jsonify(stations_list)


# In[44]:


def tobs_range():
    current_time = datetime.now()
    past_year = current_time - timedelta(weeks=100)

    tobs_st = session.query(measurement.date, measurement.tobs).filter(measurement.date > past_year)

@app.route("/api/v1.0/tobs")
def temps_json():
    results = tobs_range(measurements.tobs)
    return jsonify(results)


# In[45]:


@app.route("/api/v1.0/<start_date>/")
def temp_start(start_date):
    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurements.tobs)).filter(measurement.date >= start_date).first()
    temp_dict = {"min temp": temp[0], "max temp": temp[1], "avg temp": temp[2]}
    return jsonify(temp_dict)


# In[46]:


@app.route("/api/v1.0/<start_date>/<end_date>/")
def temp_range(start_date, end_date):
    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).first()
    temp_range_dict = {"tmin": temp[0], "tmax": temp[1], "tavg": temp[2]}
    return jsonify(temps_range_dict)


# In[47]:


if __name__ == '__main__':
    app.run(debug=True)

