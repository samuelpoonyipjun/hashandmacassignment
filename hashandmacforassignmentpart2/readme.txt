Project Overview
This repository contains the following components:
1. Main Project:
    A Python-based client-server application, consisting of the following files:
        server.py: The main server script that handles client communication.
        clientA.py: A Python script simulating how Client A interacts with the Client B and the server.
        clientB.py: A Python script simulating how Client B interacts with the Client A and the server.
2. How to run the client and server code:
    Open 3 different windows of visual studio code. In each window, run clientA, clientB and the server code respectively. On either client, send a message and see if the other client receives it. 

Directory Structure
1. Main Project (Root Directory)
    server.py: The main server script for the project.
    clientA.py: Simulates Client A's interactions with the server.
    clientB.py: Simulates Client B's interactions with the server.
2. Additional Files (Root Directory)
    readme.txt – Briefly explain how to run the program.

Notes
- The Main Project is the primary focus of our assignment, showcasing client-server-client interactions with Python.

Dependencies
- Ensure all required dependencies (as shown below) are installed before running Python scripts.
    socket: Used for network communication.
    threading: Used for handling multiple threads (e.g., message relaying, client connections).
    flask: Used when attempting to create a lightweight web server in the int-server.py file.
    cryptography: For RSA encryption, decryption, signing, and verification in clientA.py and clientB.py.
- To install flask and cryptography
    pip install flask cryptography

