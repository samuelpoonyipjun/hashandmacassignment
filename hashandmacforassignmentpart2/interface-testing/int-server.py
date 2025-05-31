from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# Socket connection to the original server
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432
BUFFER_SIZE = 4096

# Socket for communicating with the original server
server_socket = None
frontend_messages = []
backend_messages = []

# Thread to listen for messages from the original server
def listen_to_server():
    global server_socket, backend_messages
    while True:
        try:
            data = server_socket.recv(BUFFER_SIZE).decode()
            if data:
                backend_messages.append(data)  # Messages from clientB
        except Exception as e:
            print(f"Error receiving data from server: {e}")
            break

@app.route('/send', methods=['POST'])
def send_message():
    global server_socket
    data = request.json
    message = data.get('message', '')
    if message:
        try:
            server_socket.send(message.encode())  # Send frontend's message to the original server
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "No message provided"}), 400

@app.route('/receive', methods=['GET'])
def receive_messages():
    global backend_messages
    try:
        # Return backend messages for the frontend
        response = {"messages": backend_messages.copy()}
        backend_messages.clear()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    try:
        # Connect to the original server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        # Start a thread to listen for messages from the server
        threading.Thread(target=listen_to_server, daemon=True).start()

        # Start the Flask app
        app.run(host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if server_socket:
            server_socket.close()
