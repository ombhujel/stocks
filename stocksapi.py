from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import io
import base64
api_key = ''

app = Flask(__name__)

# Function to fetch stock data from API and generate JSON
def fetch_stock_data(symbol):
    # Replace with your API call logic to fetch stock data
    # Example: Using a placeholder URL
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-01-09/2024-02-10?adjusted=true&sort=asc&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming API returns JSON data
    else:
        return None

# Function to generate OHLC chart from JSON data
def generate_ohlc_chart(json_data):
    data = json_data['results']

    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for entry in data:
        # Convert timestamp to datetime in UTC
        timestamp = entry['t'] / 1000
        dates.append(datetime.fromtimestamp(timestamp, tz=timezone.utc))
        open_prices.append(entry['o'])
        high_prices.append(entry['h'])
        low_prices.append(entry['l'])
        close_prices.append(entry['c'])

    fig, ax = plt.subplots()

    # Plot candlestick chart
    ax.plot(dates, close_prices, '-', color='blue', label='Close')
    ax.plot(dates, open_prices, '-', color='green', label='Open')
    ax.plot(dates, high_prices, '-', color='black', label='High')
    ax.plot(dates, low_prices, '-', color='red', label='Low')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'OHLC Chart for {json_data["ticker"]}')

    # Display legend
    plt.legend()

    # Save plot to a BytesIO object
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Encode plot image to base64 string
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    # Close plot to release resources
    plt.close()

    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_image = None

    if request.method == 'POST':
        # Get stock symbol from form input
        symbol = request.form['symbol']

        # Fetch stock data from API
        json_data = fetch_stock_data(symbol)

        if json_data:
            # Generate OHLC chart
            plot_image = generate_ohlc_chart(json_data)

    return render_template('index.html', plot_image=plot_image)

if __name__ == '__main__':
    app.run(port=5001)
