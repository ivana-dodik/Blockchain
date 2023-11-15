import json
from crypto import decrypt_data

def format_land_book(land_book):
    # Implement the formatting logic based on your requirements
    formatted_land_book = f"Surface Area: {land_book['surface_area']}\n"
    formatted_land_book += f"Sale Price: {land_book['sale_price']}\n"
    formatted_land_book += f"Previous Owner: {land_book['previous_owner']}\n"
    formatted_land_book += f"Current Owner: {land_book['current_owner']}\n"
    formatted_land_book += f"Contract Date: {land_book['contract_date']}\n"
    formatted_land_book += f"Address: {land_book['address']}\n"
    return formatted_land_book

def format_block(block):
    index = block['index']
    timestamp = block['timestamp']
    proof = block['proof']
    previous_hash = block['previous_hash']
    block_data = block['data']

    print(f"Index: {index}")
    print(f"Timestamp: {timestamp}")
    print(f"Proof: {proof}")
    print(f"Previous Hash: {previous_hash}")


def show_formatted_blockchain():
    blockchain_filename = input("Enter the JSON filename of the blockchain: ")
    private_key_filename = input("Enter the private key filename: ")
    
    print()
    
    # blockchain_filename = 'blockchain.json'
    # private_key_filename = 'private.pem'

    try:
        with open(blockchain_filename, 'r') as file:
            blockchain_data = json.load(file)
        
        # print(blockchain_data)
        # Assuming the land book data is stored in the 'data' field of each block
        for block in blockchain_data:

            format_block(block)

            encrypted_data = block['data']

            if encrypted_data is not None:
                # Decrypt the encrypted data using the private key
                land_book_json = decrypt_data(encrypted_data)
                land_book = json.loads(land_book_json)

                formatted_land_book = format_land_book(land_book)
                print(formatted_land_book)
            else:
                print('No Block')
            print("------------------------------")

    except FileNotFoundError:
        print("File not found. Please make sure you entered the correct filenames.")

    except json.JSONDecodeError:
        print("Invalid JSON format in the blockchain file.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def console_application():
    while True:
        print("Welcome to the Land Registry Console Application!")
        print("Options:")
        print("1 - Show formatted blockchain")
        print("0 - Exit")

        option = input("Enter your option: ")

        if option == '1':
            show_formatted_blockchain()
        elif option == '0':
            break
        else:
            print("Invalid option. Please try again.")

        print()

    print("Exiting the application.")


console_application()
