import requests
import pandas as pd

def fetch_data():
    url = "https://api.blockchair.com/ethereum/transactions"
    params = {
        'limit': 10,  # Adjust the limit as necessary
        # 'key': 'your_api_key'  # Uncomment and use if you have an API key
    }

    response = requests.get(url, params=params)
    data = response.json()['data']

    df = pd.DataFrame(data)
    df.to_csv('data/raw/ethereum_transactions.csv', index=False)
    print("Ethereum transaction data fetched and saved to CSV.")
