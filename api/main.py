from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI(title="GreenOps API")

df = pd.read_csv("data/cloud_usage_enriched.csv")

model = joblib.load(
    "model/co2e_model.pkl"
)

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/metrics/summary")
def summary():
    """Summary metrics"""

    total_co2e = round(
        df["co2e_kg"].sum(), 2
    )

    total_cost = round(
        df["cost_usd"].sum(), 2
    )

    top_team = (
        df.groupby("team")["co2e_kg"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("region")["co2e_kg"]
        .sum()
        .idxmax()
    )

    return {
        "total_co2e": total_co2e,
        "total_cost": total_cost,
        "top_team": top_team,
        "top_region": top_region
    }

@app.get("/metrics/daily")
def daily():

    daily_data = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    return daily_data.to_dict(
        orient="records"
    )

@app.get("/forecast")
def forecast():
    """30-day forecast"""

    forecast_values = []

    for i in range(30):
        prediction = model.predict(
            [[0, 0, 0, i % 7]]
        )[0]

        forecast_values.append(
            round(float(prediction), 4)
        )

    return {
        "forecast": forecast_values
    }