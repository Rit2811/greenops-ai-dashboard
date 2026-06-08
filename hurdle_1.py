import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(
    'data/cloud_usage_dataset.csv',
    parse_dates=['date']
)

# Explore dataset
print("\nShape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nFirst 10 Rows:")
print(df.head(10))

print("\nNull Values:")
print(df.isnull().sum())

# Remove null rows if any
df = df.dropna()

# Cost Analysis
print("\nTotal Cost:")
print(df['cost_usd'].sum())

print("\nAverage Daily Cost:")
print(df.groupby('date')['cost_usd'].sum().mean())

# CO2e Calculation
df['co2e_kg'] = (
    (df['cpu_hours'] * 0.0002)
    + (df['storage_gb'] * 0.00006 / 30)
    + (df['data_transfer_gb'] * 0.001)
)

# Total CO2e
print("\nTotal CO2e:")
print(df['co2e_kg'].sum())

# CO2e by Service
print("\nCO2e by Service Type:")
print(df.groupby('service_type')['co2e_kg'].sum())

# CO2e by Team
print("\nCO2e by Team:")
print(df.groupby('team')['co2e_kg'].sum())

# Daily CO2e Chart
daily = df.groupby('date')['co2e_kg'].sum()

plt.figure(figsize=(10,5))
daily.plot()
plt.title("Daily CO2e")
plt.ylabel("CO2e (kg)")
plt.savefig('data/daily_co2e.png')
plt.close()

# Region CO2e Chart
region = df.groupby('region')['co2e_kg'].sum()

plt.figure(figsize=(8,5))
region.plot(kind='bar')
plt.title("CO2e by Region")
plt.ylabel("CO2e (kg)")
plt.savefig('data/co2e_by_region.png')
plt.close()

# Save enriched CSV
df.to_csv(
    'data/cloud_usage_enriched.csv',
    index=False
)

print("\nDone!")

print(df.groupby('service_type')['co2e_kg'].sum())