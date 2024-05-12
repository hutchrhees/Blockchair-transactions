import requests
import pandas as pd

def fetch_data(wallet_address=None, start_date=None, end_date=None):
    if wallet_address:
        wallet_address = wallet_address.lower()
        url = f"https://api.blockchair.com/ethereum/dashboards/address/{wallet_address}"
    else:
        url = "https://api.blockchair.com/ethereum/transactions"

    # Fetch the main transaction data
    params = {'limit': 10}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching data. Status code: {response.status_code}")
        return None





    data = response.json()

    if 'data' not in data or not data['data']:
        print("No data found or error in the API response")
        return None

    transactions = []
    transaction_hashes = []

    # Collect transaction hashes
    if wallet_address:
        wallet_data = data['data'].get(wallet_address, {})
        transactions = wallet_data.get('calls', [])
        if not transactions:
            print(f"No transactions data available for the specified wallet address: {wallet_address}")
            return None
        transaction_hashes = [tx.get('transaction_hash') for tx in transactions if tx.get('transaction_hash')]
    else:
        transactions = data['data'].get('transactions', [])
        if not transactions:
            print("No transactions data available for the general request")
            return None

    rows = []
    for hash in transaction_hashes:
        url = f"https://api.blockchair.com/ethereum/dashboards/transaction/{hash}"
        transaction_response = requests.get(url)

        if transaction_response.status_code != 200:
            print(f"Error fetching transaction details for {hash}. Status code: {transaction_response.status_code}")
            continue

        transaction_data = transaction_response.json()
        if 'data' not in transaction_data or hash not in transaction_data['data']:
            print(f"Transaction details missing for hash: {hash}")
            continue

        transaction = transaction_data['data'][hash].get('transaction', {})
        if not transaction:
            print(f"No transaction data available for hash: {hash}")
            continue

        row = {
            'block_id': transaction.get('block_id'),
            'index': transaction.get('index'),
            'hash': hash,
            'time': transaction.get('time'),
            'failed': transaction.get('failed'),
            'type': transaction.get('type'),
            'sender': transaction.get('sender'),
            'recipient': transaction.get('recipient'),
            'call_count': transaction.get('call_count'),
            'value': transaction.get('value'),
            'value_usd': transaction.get('value_usd'),
            'internal_value': transaction.get('internal_value'),
            'internal_value_usd': transaction.get('internal_value_usd'),
            'fee': transaction.get('fee'),
            'fee_usd': transaction.get('fee_usd'),
            'gas_used': transaction.get('gas_used'),
            'gas_limit': transaction.get('gas_limit'),
            'gas_price': transaction.get('gas_price'),
            'nonce': transaction.get('nonce')
        }
        rows.append(row)

    # Create a DataFrame from the collected rows
    df = pd.DataFrame(rows)
    df['Date & Time'] = pd.to_datetime(df['time'], errors='coerce')  # Ensure datetime conversion

    # Apply date filtering if both start_date and end_date are provided
    if start_date and end_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
        end_date = pd.to_datetime(end_date, errors='coerce')
        df = df[(df['Date & Time'] >= start_date) & (df['Date & Time'] <= end_date)]

    # Save the data to a CSV file
    file_name = f'ethereum_transactions_{wallet_address}.csv' if wallet_address else 'ethereum_transactions_general.csv'
    df.to_csv(f'data/raw/{file_name}', index=False)
    print(f"Data fetched and saved to {file_name}.")
    return df
