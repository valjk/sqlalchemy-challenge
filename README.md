# sqlalchemy-challenge
## I leveraged Xpert Learning assistant in my climate_starter.ipynb file in order to set the locator for the x-axis to show only 5 dates
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=len(df_precip)//25))
  
## I leveraged Xpert Learning assistant again in my app.py due to receiving a ValueError: time data 'startYYYY-MM-DD' does not match format '%Y-%m-%d'
  @app.route("/")
  def home():
     return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/startYYYY-MM-DD/endYYYY-MM-DD<br/>" #My code that was causing the error
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt<br/>" #Xpert Learning Assistant
        f"To get the temperature data for a specific date range, replace `start` and `end` in the URL above with the start and end dates in YYYY-MM-DD format.</br>"
        f"For example:/api/v1.0/2016-08-23/2017-08-23;" #Xpert Learning Assistant suggested adding documentation on how to properly display the data
     

     
