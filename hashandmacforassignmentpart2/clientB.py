import socket # used for network communication
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding # type: ignore # imports rsa algorithm and padding mechanisms
from cryptography.hazmat.primitives import hashes # type: ignore 
from cryptography.hazmat.primitives import serialization # type: ignore # converts cryptographic objects (like keys) to and from a byte representation suitable for storage or transmission

# Function to generate RSA keys
# generates a new private key with secure exponent value and a keysize of 2048 bits
# public key is part of the private key
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key() # obtains the corresponding public key from the private key
    return private_key, public_key

# Function to encrypt byte data using receiver's public key
# uses optimal assymetric encryption padding
# OAEP is a padding scheme that's used to format messages before encryption with RSA
# First a mask generation function based on SHA256 is created and a hash function for OAEP padding is created
def encrypt_data(public_key, data): 
    return public_key.encrypt(
        data.encode(), # converts the data string into bytes
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Function to decrypt byte data using receiver's private key
# OAEP padding settings are the same
def decrypt_data(private_key, encrypted_data):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

def sign_message(private_key, message): # The sender's private key is used to sign the message
    return private_key.sign( # returns the signature as a byte string
        message.encode(),  # Convert the message to bytes for signing
        padding.PSS( # secure padding scheme for RSA
            mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function (MGF1) with SHA-256
            salt_length=padding.PSS.MAX_LENGTH  # Use the maximum permissible salt length
        ),
        hashes.SHA256()  # Use SHA-256 as the hashing algorithm
    )
# verifies integrity and authenticity of message using sender's public key and signature
def verify_signature(public_key, message, signature): # signature is verified using the sender's public key
    try:
        public_key.verify( # checks if signature matches the original message
            signature,  # Signature to validate
            message.encode(),  # The original message (converted to bytes)
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),  # Same MGF1 settings as used in `sign_message`
                salt_length=padding.PSS.MAX_LENGTH  # Same salt length
            ),
            hashes.SHA256()  # Same hashing algorithm as in `sign_message`
        )
        return True  # If verification is successful
    except Exception:  # Catch any verification failure
        return False  # Return False if verification fails

# Thread function for sending messages
def send_messages(client_socket, private_key, other_client_public_key):
    while True:
        # Prompts for user to input a message
        message = input("Input Message (Type exit to close connection): ")
        if message.lower() == "exit": # closes the client socket and the connection if message input is exit
            print("Closing connection...")
            client_socket.close()
            break
        # Sign the message using the private key
        signature = sign_message(private_key, message)
        # Encrypt the message using the other client's public key and sends encrypted message to server
        encrypted_message = encrypt_data(other_client_public_key, message)
        # combines the signature and encrypted message into a payload and sends to server
        # || is used to seperate the signature from the encrypted message
        client_socket.send(signature + b'||' + encrypted_message)

# Thread function for receiving messages
def receive_messages(client_socket, private_key, other_client_public_key):
    while True:
        try:
            # Receive an encrypted message from the other client through the server
            payload = client_socket.recv(4096) # the payload combined is 4096 bytes long
            if not payload:  # If no data is received, it implies the connection is closed
                print("\nThe other client has closed the connection.")
                break
            received_signature, encrypted_message = payload.split(b'||') # now seperates the signature and encrypted response and saves them under different variables
            # Decrypt the message using the private key
            decrypted_message = decrypt_data(private_key, encrypted_message)   
            # verify signature function returns either true or false depending on whether message could be verified using public key      
            if verify_signature(other_client_public_key, decrypted_message, received_signature):
                print(f"\nClient A: {decrypted_message}")
                print("Input message (Type exit to close connection): ", end="", flush=True)#flush is true line is so that the input prompt will keep appearing
            else:
                print("Received message with an invalid signature.")
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close() # Once when client breaks out of while loop, close the connection

# Client function
# Host IP, port number are configured and user is prompted to input message
def start_clientB(host='127.0.0.1', port=65432):
    # Generate RSA keys
    # the value under the variable private_key will be the first value returned by the function generate_keys
    private_key, public_key = generate_keys()

    # Serialize the public key to send to the server
    # Encodes the key into human readable text and specifies the public key format
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
# creates a TCP/IP socket and connects the socket to the server at the given address and port number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server!")

    # Send serialized public key to the server
    client_socket.send(serialized_public_key)
    print("Public key sent to the server.")

    # Receive the other client's public key, up to 2048 bytes
    # Converts the received public key from PEM into usable public key object (deserialise the key)
    other_client_public_key_pem = client_socket.recv(2048)
    other_client_public_key = serialization.load_pem_public_key(other_client_public_key_pem)
    print("Received the other client's public key.")
    # Start threads for sending and receiving messages
    threading.Thread(target=send_messages, args=(client_socket, private_key, other_client_public_key)).start()
    threading.Thread(target=receive_messages, args=(client_socket, private_key, other_client_public_key)).start()

start_clientB()