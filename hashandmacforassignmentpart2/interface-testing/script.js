const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const serverUrl = 'http://127.0.0.1:5000'; // intermediary server URL

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        // display the sent message in the chat
        const msg = document.createElement('div');
        msg.classList.add('message', 'sent');
        msg.textContent = message;
        messagesDiv.appendChild(msg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // send the message to the intermediary server
        try {
            await fetch(`${serverUrl}/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
        } catch (error) {
            console.error('Error sending message:', error);
        }

        messageInput.value = '';
    }
}

async function fetchMessages() {
    try {
        const response = await fetch(`${serverUrl}/receive`);
        const data = await response.json();

        if (data.messages) {
            data.messages.forEach((message) => {
                const msg = document.createElement('div');
                msg.classList.add('message', 'received');
                msg.textContent = message;
                messagesDiv.appendChild(msg);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// poll the intermediary server for new messages every second
setInterval(fetchMessages, 1000);