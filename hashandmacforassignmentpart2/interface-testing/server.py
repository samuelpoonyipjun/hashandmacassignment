import socket # used for network communication
import threading # library used to handle multiple clients simultaneously using multiple seperate threads

def exchange_keys(client1, client2): # function to exchange keys between both clients
    try:
        # Receive public keys from both clients
        client1_public_key_pem = client1.recv(2048)
        client2_public_key_pem = client2.recv(2048)
        print("Received public keys from both clients.")

        # Send Client1's public key to Client2 and vice versa
        client2.send(client1_public_key_pem)
        client1.send(client2_public_key_pem)
        print("Exchanged public keys between clients.")
    except Exception as e: #raises an error exception when exchange failed
        print(f"Error during key exchange: {e}")
        client1.close() # closes both clients when key exchange error occurs
        client2.close()

def relay_messages(source_client, target_client):
    # passes the message between source and target client
    try:
        while True:
            data = source_client.recv(2048) # data is received by the source client
            if not data:  # If no data is received, assume the client has disconnected
                break
            target_client.send(data) # send the message from the source client to target
    except Exception as e: # otherwise print error message
        print(f"Error relaying messages: {e}")
    finally:
        source_client.close()
        target_client.close()

# Handle communication between two clients
# tries and prints any error as exception and closes clients
def handle_client(client1, client2):
    try:
        # Exchange public keys between the clients
        exchange_keys(client1, client2)
        # Start threads to handle bidirectional communication
        print("Starting message relay between clients.")
        threading.Thread(target=relay_messages, args=(client1, client2)).start()
        threading.Thread(target=relay_messages, args=(client2, client1)).start()
    except Exception as e:
        print(f"Error handling clients: {e}")
        client1.close()
        client2.close()
# A TCP/IP socket is created with the host and port number
# The socket allows 2 clients to listen at the same time
# Handles clients and starts up both threads
def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server is listening for clients...")
    # accept function blocks until a client connects to the socket
    # function returns a client socket and the client's address
    client1, addr1 = server_socket.accept()
    print(f"Client1 connected from {addr1}")
    client2, addr2 = server_socket.accept()
    print(f"Client2 connected from {addr2}")
    handle_client(client1, client2)

# run the server
start_server()
