from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from blockchain import Blockchain
from crypto import load_private_key

def get_wallet_balance(blockchain, wallet_private_key):
    # Iterate through transactions to calculate wallet balance
    wallet_address = blockchain.generate_address(wallet_private_key.public_key())
    balance = 0

    for block in blockchain.chain:
        for transaction in block['transactions']:
            if transaction['receiver'] == wallet_address:
                balance += transaction['amount']
            if transaction['sender'] == wallet_address:
                balance -= transaction['amount']

    return balance

def get_wallet_transactions(blockchain, wallet_private_key):
    # Retrieve transactions involving the wallet
    wallet_address = blockchain.generate_address(wallet_private_key.public_key())
    transactions = []

    for block in blockchain.chain:
        for transaction in block['transactions']:
            if transaction['sender'] == wallet_address or transaction['receiver'] == wallet_address:
                transactions.append(transaction)

    return transactions

while True:
    print("Options:")
    print("0 - Exit")
    print("1 - Check Wallet")
    choice = input("Enter your choice: ")

    if choice == "0":
        print("Exiting...")
        break

    elif choice == "1":
        priv_key_path = input("Enter the path to the private key: ")
        blockchain_path = input("Enter the path to the blockchain JSON file: ")

        try:
            wallet_private_key = load_private_key(priv_key_path)
            blockchain = Blockchain(priv_key_path)
            blockchain.load_blockchain(blockchain_path)

            wallet_balance = get_wallet_balance(blockchain, wallet_private_key)
            wallet_transactions = get_wallet_transactions(blockchain, wallet_private_key)

            print("Wallet Balance:", wallet_balance)
            print("Wallet Transactions:", wallet_transactions)

        except Exception as e:
            print("Error:", str(e))

    else:
        print("Invalid choice. Please try again.")
