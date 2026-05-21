from flask import Flask, render_template
import pandas as pd
from google.cloud import storage
import io

app = Flask(__name__)

BUCKET_NAME = "date-meteo-istorice-bucket" 
#storage_client = storage.Client.from_service_account_json("credentials/vm-deb9-2563c9152a85.json")
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

#Citeste csv din google cloud storage
def read_csv_from_gcs(blob_path, **kwargs):
    blob = bucket.blob(blob_path)
    data = blob.download_as_text()
    return pd.read_csv(io.StringIO(data), **kwargs)

df_station = read_csv_from_gcs("stations.txt", skiprows=17)

@app.route("/")
def home():
    return render_template("home.html",
                           data=df_station[["STAID", "STANAME                                 "]].to_html())

@app.route("/api/v1/<station>/<date>")
def api(station, date):
    filename = f"TG_STAID{station.zfill(6)}.txt"
    
    df = read_csv_from_gcs(filename, skiprows=20, parse_dates=["    DATE"])
    
    date_df = df.loc[df["    DATE"] == date]
    raw_temperature = date_df["   TG"]
    
    if raw_temperature.empty:
        return {"error": "No data for this date"}
        
    temperature = raw_temperature.squeeze() / 10

    if temperature == -999.9:
        temperature = "LOST"

    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }

@app.route("/api/v1/<station>")
def all_data(station):
    filename = f"TG_STAID{str(station).zfill(6)}.txt"
    
    df = read_csv_from_gcs(filename, skiprows=20)
    df["   TG"] = df["   TG"] / 10
    
    result = df.to_dict(orient="records")
    for row in result:
        if row["   TG"] == -999.9:
            row["   TG"] = "LOST"
            
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def on_year(station, year):
    filename = f"TG_STAID{str(station).zfill(6)}.txt"
    
    df = read_csv_from_gcs(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    
    return result

if __name__ == "__main__":
    app.run(debug=True)