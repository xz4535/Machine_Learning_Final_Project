# https://www.kaggle.com/code/anandhuh/extracting-visualizing-stock-data-2022
# pip install yfinance
# pip install bs4

import pandas as pd

import yfinance as yf
import requests
from bs4 import BeautifulSoup

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price ($)", "Historical Revenue ($)"), vertical_spacing = .5)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($ Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=1000, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

# Define your company tickers
company_tickers = ['ADS.DE', 'GOOGL', 'TSLA']  # Replace with actual tickers

# Define the period for your data
period = '2y'  # Two years period
interval = '1d'  # Hourly data

for ticker in company_tickers:
    # Fetch the stock data
    stock_data = yf.Ticker(ticker)
    stock_data_hourly = stock_data.history(period=period, interval=interval)

    # Filter and save the data for 2023 and 2024
    for year in [2023, 2024]:
        stock_data_year = stock_data_hourly[stock_data_hourly.index.year == year]
        stock_data_year.to_csv(f'{ticker}_stock_data_day_{year}.csv', index=True)

    # Now, read the saved data back into DataFrames
    data_2023 = pd.read_csv(f'{ticker}_stock_data_day_2023.csv')
    data_2024 = pd.read_csv(f'{ticker}_stock_data_day_2024.csv')

    # Concatenate the dataframes for 2023 and 2024
    combined_data = pd.concat([data_2023, data_2024], ignore_index=True)

# Save the combined dataframe to a new CSV file for the company
    combined_data.to_csv(f'{ticker}_stock_data_day_2023_2024.csv', index=False)

    print(f'Combined hourly data for {ticker} saved to {ticker}_stock_data_day_2023_2024.csv')


# # Using the Ticker function to create a ticker object.
# # ticker symbol of Google is GOOGL for Class A shares or GOOG for Class C shares
# data = yf.ticker('TSLA')  # You can replace 'GOOGL' with 'GOOG' if you prefer

# tesla_data_hour = data.history(period='2y', interval='1h')

# # Filter for the year 2022
# tesla_data_2022 = tesla_data_hour.loc[tesla_data_hour.index.year == 2022]
# # Save the 2022 data to a CSV file
# tesla_data_2022.to_csv('tesla_stock_data_2022.csv', index=True)

# # Filter for the year 2023
# tesla_data_2023 = tesla_data_hour.loc[tesla_data_hour.index.year == 2023]
# # Save the 2023 data to a CSV file
# tesla_data_2023.to_csv('tesla_stock_data_2023.csv', index=True)


# # Filter for the year 2024
# tesla_data_2024 = tesla_data_hour.loc[tesla_data_hour.index.year == 2024]
# # Save the 2024 data to a CSV file
# tesla_data_2024.to_csv('tesla_stock_data_2024.csv', index=True)

# # # Save the DataFrame to a CSV file
# # google_data_min.to_csv('google_stock_data.csv', index=False)

# # Print out information to confirm the process
# print("Saved 2023 data with {} rows".format(len(tesla_data_2023)))
# print("Saved 2024 data with {} rows".format(len(tesla_data_2024)))



