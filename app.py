from flask import Flask, jsonify, request
from flask_cors import CORS

import requests
api_key = ''

app = Flask(__name__)
CORS(app)

# Replace with your API call logic to fetch stock data
def fetch_stock_data(symbol):
    # Example: Using a placeholder URL
    url = f'https://api.polygon.io/v1/open-close/{symbol}/2023-01-09?adjusted=true&apiKey={api_key}'
    # url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-01-09/2024-02-10?adjusted=true&sort=asc&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming API returns JSON data
    else:
        return None

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400

    json_data = fetch_stock_data(symbol)
    if json_data:
        return jsonify(json_data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
