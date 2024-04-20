import pandas as pd
from alpha_vantage.timeseries import TimeSeries
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

# Replace 'YOUR_API_KEY' with your actual API Key from Alpha Vantage
api_key = '1XOATWW9O4KGTMO4'

# Initialize the TimeSeries class with your key and output format
ts = TimeSeries(key=api_key, output_format='pandas')

# Get the data (this example retrieves data, but you might be limited to the last 1-2 months of intraday data)
# The `outputsize='full'` might not be supported for minute-level data with a free API key
data, meta_data = ts.get_intraday(symbol='GOOGL', interval='60min', outputsize='full')

# Check if the call was successful
if data.empty:
    print("No data returned from the API.")
else:
    print("Data successfully retrieved.")

# Convert the index to datetime if it isn't already
data.index = pd.to_datetime(data.index)

# Filter data for 2023
data_2023 = data[data.index.year == 2023]
# Reset the index if you want to save the datetime as a column
data_2023.reset_index(inplace=True)
# Save the 2023 DataFrame to a CSV file
data_2023.to_csv('alpha_google_stock_data_2023.csv', index=False)

# Filter data for 2024
data_2024 = data[data.index.year == 2024]
# Reset the index if you want to save the datetime as a column
data_2024.reset_index(inplace=True)
# Save the 2024 DataFrame to a CSV file
data_2024.to_csv('alpha_google_stock_data_2024.csv', index=False)

# Print out information to confirm the process
print("Saved 2023 data with {} rows".format(len(data_2023)))
print("Saved 2024 data with {} rows".format(len(data_2024)))