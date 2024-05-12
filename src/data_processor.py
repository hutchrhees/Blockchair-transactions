import pandas as pd


def process_data(file_name):
    raw_path = f'data/raw/{file_name}'
    df = pd.read_csv(raw_path)
    processed_path = 'data/processed/processed_ethereum_data.xlsx'
    df.to_excel(processed_path, index=False)
    print(f"Data processed and saved to {processed_path}.")
