from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
import io
import os

load_dotenv()

CONN_STR = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING"
)

client = BlobServiceClient.from_connection_string(
    CONN_STR
)

blob = (
    client
    .get_container_client("greenops-data")
    .get_blob_client("cloud_usage_enriched.csv")
)

data = blob.download_blob().readall()

df = pd.read_csv(io.BytesIO(data))

print("Shape:", df.shape)
print("Total CO2e:", df["co2e_kg"].sum())