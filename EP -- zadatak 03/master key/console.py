from blockchain import Blockchain
from bitcoinlib.keys import HDKey, verify

def get_wallet_balance(blockchain):
    # Iterate through transactions to calculate wallet balance
    wallet_address = blockchain.get_address()
    balance = 0

    for block in blockchain.chain:
        for transaction in block['transactions']:
            if transaction['receiver'] == wallet_address:
                balance += transaction['amount']
            if transaction['sender'] == wallet_address:
                balance -= transaction['amount']

    return balance

def get_wallet_transactions(blockchain):
    # Retrieve transactions involving the wallet
    wallet_address = blockchain.get_address()
    transactions = []

    for block in blockchain.chain:
        for transaction in block['transactions']:
            if transaction['sender'] == wallet_address or transaction['receiver'] == wallet_address:
                transactions.append(transaction)

    return transactions

def check_transactions(transactions):
    for transaction in transactions:
        txid = transaction['txid']
        signature = transaction['signature']
        public_key = HDKey(transaction['public_key'])

        verification = verify(txid, signature, public_key)
        if verification != True:
            return False
    
    return True

while True:
    print("Options:")
    print("0 - Exit")
    print("1 - Check Wallet")
    choice = input("Enter your choice: ")

    if choice == "0":
        print("Exiting...")
        break

    elif choice == "1":
        mnemonic_words_path = input("Enter the path to the mnemonic words: ")
        blockchain_path = input("Enter the path to the blockchain JSON file: ")

        try:
            with open(mnemonic_words_path, 'r') as file:
                mnemonic_words = file.readline()

            blockchain = Blockchain(mnemonic_words)
            blockchain.load_blockchain(blockchain_path)

            wallet_balance = get_wallet_balance(blockchain)
            wallet_transactions = get_wallet_transactions(blockchain)
            print(type(wallet_transactions))
            print("Wallet Balance:", wallet_balance)
            print("Wallet Transactions:", wallet_transactions)

            # Check if transactions are valid:
            is_valid_transactions = check_transactions(wallet_transactions)
            print("All transactions are valid?:", is_valid_transactions)

        except Exception as e:
            print("Error:", str(e))

    else:
        print("Invalid choice. Please try again.")
