import pandas as pd
import io
from google.cloud import storage
from main import read_csv_from_gcs

#Se testeaza extragerea a primelor 5 statii meteo din bucket folosind functia din main.py
def test_extract_from_gcs():

    BUCKET_NAME = "date-meteo-istorice-bucket" 
    storage_client = storage.Client.from_service_account_json(r"C:\Users\Victor\Downloads\vm-deb9-2563c9152a85.json")
    bucket = storage_client.bucket(BUCKET_NAME)

    df_station = read_csv_from_gcs("stations.txt", skiprows=17)

    print("Conexiunea cu GCS și extragerea au fost reușite. Primele 5 înregistrări:")
    print(df_station.head())

if __name__ == "__main__":
    test_extract_from_gcs()