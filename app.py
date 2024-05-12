from flask import Flask, request, jsonify, render_template
from src.data_fetcher import fetch_data
from src.data_processor import process_data
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    wallet_address = data['wallet_address']
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if wallet_address:
        try:
            fetch_data(wallet_address, start_date, end_date)
            csv_file_name = f'ethereum_transactions_{wallet_address}.csv'
            process_data(csv_file_name)

            # Read the processed file back into a DataFrame to send to front-end
            processed_path = f'data/processed/processed_ethereum_data.xlsx'
            df = pd.read_excel(processed_path)

            # Convert DataFrame to HTML table for easy display
            html_table = df.to_html(classes='table table-striped', index=False, border=0)
            return jsonify({'html_table': html_table, 'message': 'Data fetched and processed successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid or empty wallet address'}), 400

if __name__ == '__main__':
    app.run(debug=True)
