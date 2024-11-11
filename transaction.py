import re
from pymongo import MongoClient

def parse_transaction_message(message):
    # Regular expressions to match the transaction details
    amount_pattern = r'\b\d+\.\d{2}\b'
    transaction_type_pattern = r'\b(credited|debited|credit|debit)\b'
    account_number_pattern = r'\bending in (\d{4})\b'
    date_pattern = r'\b(\d{2} \w+ \d{4})\b'
    time_pattern = r'\b(\d{2}:\d{2})\b'

    # Find all matches in the message
    amount_match = re.search(amount_pattern, message)
    transaction_type_match = re.search(transaction_type_pattern, message)
    account_number_match = re.search(account_number_pattern, message)
    date_match = re.search(date_pattern, message)
    time_match = re.search(time_pattern, message)

    # Extract the matched values
    amount = amount_match.group(0) if amount_match else None
    transaction_type = transaction_type_match.group(0) if transaction_type_match else None
    account_number = account_number_match.group(1) if account_number_match else None
    date = date_match.group(1) if date_match else None
    time = time_match.group(1) if time_match else None

    return {
        'amount': amount,
        'transaction_type': transaction_type,
        'account_number': account_number,
        'date': date,
        'time': time
    }

def insert_transaction(transaction):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)  # Adjust the host and port if needed
    db = client['your_database_name']  # Replace with your database name
    collection_name = f'acc{transaction["account_number"]}'  # Collection name based on account number
    collection = db[collection_name]

    # Insert the transaction document
    collection.insert_one(transaction)

def main():
    with open('transactions.txt', 'r') as file:
        message = file.read()

    transaction_details = parse_transaction_message(message)

    # Print transaction details (optional)
    print(transaction_details)

    # Insert the transaction into the database
    insert_transaction(transaction_details)

if __name__ == '__main__':
    main()
