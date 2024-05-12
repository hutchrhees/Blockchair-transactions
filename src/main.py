from data_fetcher import fetch_data
from data_processor import process_data

def main():
    fetch_data('0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae')
    process_data('ethereum_transactions_0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae.csv')

if __name__ == "__main__":
    main()
