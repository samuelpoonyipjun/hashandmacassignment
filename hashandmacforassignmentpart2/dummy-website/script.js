const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');

// mocked storage for messages
let mockMessages = [];

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        // display the sent message in the chat
        const msg = document.createElement('div');
        msg.classList.add('message', 'sent');
        msg.textContent = message;
        messagesDiv.appendChild(msg);

        // scroll to the bottom when a message is sent
        scrollToBottom();

        // add the message to the mock storage
        mockMessages.push({ sender: 'You', text: message });

        // clear the input field
        messageInput.value = '';
    }
}

// simulate fetching messages (other user's messages)
function fetchMessages() {
    try {
        // simulate fetching new messages
        const newMessages = [{ text: `Mock message ${mockMessages.length + 1}`, sender: 'Other' }];
        if (newMessages.length > 0) {
            newMessages.forEach(({ sender, text }) => {
                const msg = document.createElement('div');
                msg.classList.add('message', sender === 'You' ? 'sent' : 'received');
                msg.textContent = text;
                messagesDiv.appendChild(msg);
            });

            // scroll to the bottom only when new messages are received
            scrollToBottom();

            // add the new messages to mock storage
            mockMessages.push(...newMessages);
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

// helper function to scroll to the bottom
function scrollToBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// set up periodic fetching of messages
setInterval(fetchMessages, 2000);

// handle pressing Enter to send a message
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
