import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

# =========================
# Load Dataset
# =========================

df = pd.read_csv("data/cloud_usage_enriched.csv")

# Convert date column
df["date"] = pd.to_datetime(
    df["date"],
    format="%d/%m/%Y"
)

# =========================
# Daily Aggregation
# =========================

daily = (
    df.groupby("date")["co2e_kg"]
    .sum()
    .reset_index()
)

# =========================
# Feature Engineering
# =========================

daily["lag_7"] = daily["co2e_kg"].shift(7)
daily["lag_14"] = daily["co2e_kg"].shift(14)

daily["rolling_7"] = (
    daily["co2e_kg"]
    .rolling(window=7)
    .mean()
)

daily["dow"] = daily["date"].dt.dayofweek

# Remove rows with NaN values
daily = daily.dropna()

# =========================
# Features and Target
# =========================

X = daily[[
    "lag_7",
    "lag_14",
    "rolling_7",
    "dow"
]]

y = daily["co2e_kg"]

# =========================
# Train/Test Split
# Last 30 Days = Test Set
# =========================

X_train = X.iloc[:-30]
X_test = X.iloc[-30:]

y_train = y.iloc[:-30]
y_test = y.iloc[-30:]

# =========================
# Train Model
# =========================

model = LinearRegression()

model.fit(
    X_train,
    y_train
)

# =========================
# Predictions
# =========================

y_pred = model.predict(X_test)

# =========================
# RMSE
# =========================

rmse = root_mean_squared_error(
    y_test,
    y_pred
)

print("\nRMSE:", round(rmse, 6))

mean_daily_co2e = y_test.mean()

print(
    "Mean Daily CO2e:",
    round(mean_daily_co2e, 6)
)

if rmse < (0.10 * mean_daily_co2e):
    print(
        "RMSE is below 10% of mean daily CO2e ✅"
    )
else:
    print(
        "RMSE is above 10% of mean daily CO2e ⚠️"
    )

# =========================
# Plot Actual vs Predicted
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    y_test.values,
    label="Actual"
)

plt.plot(
    y_pred,
    label="Predicted"
)

plt.title(
    "Actual vs Predicted CO2e"
)

plt.xlabel("Days")
plt.ylabel("CO2e (kg)")
plt.legend()
plt.grid(True)

plt.savefig(
    "model/forecast_plot.png"
)

plt.close()

# =========================
# Save Model
# =========================

joblib.dump(
    model,
    "model/co2e_model.pkl"
)

print(
    "\nForecast plot saved:"
)

print(
    "model/forecast_plot.png"
)

print(
    "\nModel saved:"
)

print(
    "model/co2e_model.pkl"
)