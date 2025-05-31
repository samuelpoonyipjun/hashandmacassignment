Project Overview
This repository contains the following components:
1. Main Project:
    A Python-based client-server application, consisting of the following files:
        server.py: The main server script that handles client communication.
        clientA.py: A Python script simulating how Client A interacts with the Client B and the server.
        clientB.py: A Python script simulating how Client B interacts with the Client A and the server.
2. Dummy Website:
    A static website created with HTML, CSS, and JavaScript. This serves as a demonstration of what the website should look like if integration is successful.
3. Interface Testing:
    A interface testing setup. This was an attempt to implement the main project into a web-based interface.
4. How to run the client and server code:
    Open 3 different windows of visual studio code. In each window, run clientA, clientB and the server code respectively. On either client, send a message and see if the other client receives it. 

Directory Structure
1. Main Project (Root Directory)
    server.py: The main server script for the project.
    clientA.py: Simulates Client A's interactions with the server.
    clientB.py: Simulates Client B's interactions with the server.
2. dummy-website
    index.html: The main HTML file for the dummy website.
    main.css: CSS providing overall styling for the website.
    messages.css: CSS specifically for handling message-based UI elements.
    script.js: JavaScript file for interactivity and dynamic content.
3. interface-testing
    clientA.py: Python script from main project.
    clientB.py: Python script from main project.
    int-server.py: Python script acting as the server for interface testing.
    index.html: HTML file providing a web-based interface for the testing environment.
    main.css: CSS for the interface's design.
    script.js: JavaScript for interactivity in the web interface.
    README.md: Markdown version of the documentation (includes how to run it).
    server.py: Serve script from main project.
4. Additional Files (Root Directory)
    readme.txt – Briefly explain how to run the program.
    contributions.txt - List the work completed by each member.

Notes
- The Main Project is the primary focus of our assignment, showcasing client-server-client interactions with Python.
- The Dummy Website and Interface Testing directories provide examples of web development and interface testing.

Dependencies
- Ensure all required dependencies (as shown below) are installed before running Python scripts.
    socket: Used for network communication.
    threading: Used for handling multiple threads (e.g., message relaying, client connections).
    flask: Used when attempting to create a lightweight web server in the int-server.py file.
    cryptography: For RSA encryption, decryption, signing, and verification in clientA.py and clientB.py.
- To install flask and cryptography
    pip install flask cryptography