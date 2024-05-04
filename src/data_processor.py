import pandas as pd

def process_data():
    df = pd.read_csv('data/raw/ethereum_transactions.csv')
    # Perform any needed transformations here
    processed_path = 'data/processed/processed_ethereum_data.xlsx'
    df.to_excel(processed_path, index=False)
    print(f"Ethereum data processed and saved to {processed_path}.")
