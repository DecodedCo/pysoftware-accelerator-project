import json
import numpy as np
from datetime import datetime, timedelta

import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def simulate_electricity_prices(years):
    days_in_year = 365
    initial_price = 14.0                    # Starting price in pence per kWh
    price_trend = 0.02                      # Annual price increase (2%)
    seasonal_variation_amplitude = 2.0      # Amplitude of seasonal variation
    price_fluctuation_stddev = 0.9          # Standard deviation of price fluctuations

    timestamps = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(days_in_year * years)]

    prices = []
    for i in range(len(timestamps)):
        day_of_year = timestamps[i].timetuple().tm_yday
        price = (
            initial_price
            + day_of_year * (price_trend / days_in_year)
            + seasonal_variation_amplitude * np.sin(2 * np.pi * day_of_year / days_in_year)
            + np.random.normal(0, price_fluctuation_stddev)
        )
        prices.append(round(max(0, price), 2))  # Ensure prices are non-negative

    return timestamps, prices




timestamps, prices = simulate_electricity_prices(years=1)

print(timestamps[:10])
print(prices[:10])

