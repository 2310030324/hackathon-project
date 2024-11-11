import re
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  # Replace with your database name

def parse_transaction_message(message):
    amount_pattern = r'\b\d+\.\d{2}\b'
    transaction_type_pattern = r'\b(credited|debited|credit|debit)\b'
    account_number_pattern = r'\b\d{4}\b'
    date_pattern = r'\b\d{1,2} \w{3} \d{4}\b'
    time_pattern = r'\b\d{1,2}:\d{2}\b'

    # Find all matches in the message
    amount_match = re.search(amount_pattern, message)
    transaction_type_match = re.search(transaction_type_pattern, message)
    account_number_match = re.search(account_number_pattern, message)
    date_match = re.search(date_pattern, message)
    time_match = re.search(time_pattern, message)

    amount = amount_match.group(0) if amount_match else None
    transaction_type = transaction_type_match.group(0) if transaction_type_match else None
    account_number = account_number_match.group(0) if account_number_match else None
    date = date_match.group(0) if date_match else None
    time = time_match.group(0) if time_match else None

    return {
        'amount': amount,
        'transaction_type': transaction_type,
        'account_number': account_number,
        'date': date,
        'time': time
    }

def insert_transaction(transaction_data):
    collection_name = f'acc{transaction_data["account_number"]}'
    db[collection_name].insert_one(transaction_data)

@app.route('/', methods=['GET', 'POST'])
def home():
    transactions = []
    if request.method == 'POST':
        last4digits = request.form['account_number']
        collection_name = f'acc{last4digits}'
        transactions = list(db[collection_name].find())
    return render_template('index.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
