# # importing flask as a dependency ((9.4.3))
# from flask import Flask

# # creating a new flask app instance ((9.4.3))
# app = Flask(__name__)

## creating flask routes
# @app.route('/')
# def hello_world():
#     return 'Hello world'

# Setting uo the flask weather app ((9.5.1))
import datetime as dt
import numpy as np
import pandas as pd

# Importing SQLAlchemy ((9.5.1))
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# impoting Flask ((9.5.1))
from flask import Flask, jsonify

# Setting up the Database ((9.5.1)) / ((9.1.5))
engine = create_engine("sqlite:///hawaii.sqlite")

# Setting up a foundation to build on is SQLAchemy,
    # reflect an existing database into a new module ((9.5.1)) / ((9.1.5))
Base = automap_base()

# Reflecting on table using the prepare() function,
    # reflect the table ((9.5.1)) / ((9.1.5))
Base.prepare(engine, reflect=True)

# Saving references to each table ((9.5.1)) / ((9.1.5))
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating the session (link) ((9.5.1)) / ((9.1.5))
session = Session(engine)

# Setting up Flask ((9.5.1))
app = Flask(__name__)

# Creating flask routes ((9.5.2)) / ((9.4.3))
@app.route("/")

# Adding the route information ((9.5.2))
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! 
    Available Routes: 
    /api/v1.0/precipitation 
    /api/v1.0/stations 
    /api/v1.0/tobs 
    /api/v1.0/temp/start/end 
    ''')

# # Output http://
# if __name__ == '__main__':
#     app.run()

# Creating a new route for percipitation ((9.5.3))
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# # Output http://
# if __name__ == '__main__':
#     app.run()

# Creating a new route for station ((9.5.4))
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# # Output http://
# if __name__ == '__main__':
#     app.run()

# Creating a new route for tobs/temperature observations for the previous year ((9.5.5))
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Output http://
if __name__ == '__main__':
    app.run()

# Creating a new route for the min, avg, and max temp ((9.5.6)) 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Add parameters to `stats()`: `start` and `end` parameters
def stats(start=None, end=None):
	# Query: min, avg, max temps; create list called `sel`
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

	# Add `if-not` statement to determine start/end date
	if not end:
		results = session.query(*sel).\
			filter(Measurement.date >= start).\
			filter(Measurement.date <= end).all()
		temps = list(np.ravel(results))
	return jsonify(temps=temps)

		#NOTE: (*sel) - asterik indicates multiple results from query: minimum, average, and maximum temperatures

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    
# Output http://
if __name__ == '__main__':
    app.run()

	#NOTE: /api/v1.0/temp/start/end route -> [null,null,null]
	#NOTE: Add following to path to address in browser:
		# /api/v1.0/temp/2017-06-01/2017-06-30
		# result: ["temps":[71.0,77.21989528795811,83.0]]