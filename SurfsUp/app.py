# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
import numpy as np
import sqlalchemy
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
     return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt<br/>"
        f"To get the temperature data for a specific date range, replace `start` and `end` in the URL above with the start and end dates in YYYY-MM-DD format.</br>"
        f"For example:/api/v1.0/2016-08-23/2017-08-23;"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value"""
    
    # Get the most recent date from the database
    most_recent_date_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Check if we received a Row object
    if most_recent_date_row is None:
        return jsonify({"error": "No data found."}), 404

    # Extract the date from the Row object and convert it to a string
    most_recent_date = str(most_recent_date_row[0]) 
    
    # Print the type of most_recent_date to the console 
    print(type(most_recent_date)) 

    # Calculate the date one year ago
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query the database for precipitation data within the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Convert the results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    # Close the session
    session.close()

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
     """Return a JSON list of stations from the dataset."""
     with engine.connect() as conn:
          station_results = conn.execute("SELECT station FROM Station").fetchall()
          stations_list = [result[0] for result in station_results]
     
     session.close()

     return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
     """Return the temperature observations for the previous year of the most active station."""
     session = Session(engine)
     most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()
     
     most_recent_date = session.query(Measurement.date).\
        filter(Measurement.station == most_active_station[0]).\
        order_by(Measurement.date.desc()).\
        first()
     
     one_year_ago = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)

     results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= one_year_ago).\
        all()
     
     tobs_data = {date: tobs for date, tobs in results}

     session.close()

     return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temperature_start(start):
      """Return the minimum, average, and maximum temperatures for dates greater than or equal to the start date."""
      session = Session(engine)
      start_date = datetime.strptime(start, 'YYYY-MM-DD')
      results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        all()

      temperature_data = { "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
        }
      
      session.close()
      
      return jsonify(temperature_data)

@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    session = Session(engine)

    start_date = datetime.strptime(start, '%Y-%m-%d')  
    end_date = datetime.strptime(end, '%Y-%m-%d')  
   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()

    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    session.close()

    return jsonify(temperature_data)



if __name__ == '__main__':
    app.run(debug=True)