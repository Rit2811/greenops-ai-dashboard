import streamlit as st
import pandas as pd
import requests

st.title("GreenOps Dashboard")

summary = requests.get(
    "http://127.0.0.1:8000/metrics/summary"
).json()

st.metric(
    "Total CO2e (kg)",
    summary["total_co2e"]
)

st.metric(
    "Total Cost (USD)",
    summary["total_cost"]
)

st.metric(
    "Highest Emission Team",
    summary["top_team"]
)

daily = requests.get(
    "http://127.0.0.1:8000/metrics/daily"
).json()

daily_df = pd.DataFrame(
    daily
)

st.subheader("Daily CO2e")

st.line_chart(
    daily_df["co2e_kg"]
)

if st.button("Show Forecast"):

    forecast = requests.get(
        "http://127.0.0.1:8000/forecast"
    ).json()

    forecast_df = pd.DataFrame(
        forecast["forecast"],
        columns=["predicted_co2e"]
    )

    st.subheader(
        "30-Day Forecast"
    )

    st.line_chart(
        forecast_df
    )