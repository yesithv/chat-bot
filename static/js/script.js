// Section: get the Id of the talking container
const messagesContainer = document.getElementById('messages-container');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
//

//Section: function to creat the dialogue window
const addMessage = (message, role, imgSrc) => {
  // creat elements in the dialogue window
  const messageElement = document.createElement('div');
  const textElement = document.createElement('p');
  messageElement.className = `message ${role}`;
  const imgElement = document.createElement('img');
  imgElement.src = `${imgSrc}`;
  // append the image and message to the message element
  messageElement.appendChild(imgElement);
  textElement.innerText = message;
  messageElement.appendChild(textElement);
  messagesContainer.appendChild(messageElement);
  // creat the ending of the message
  var clearDiv = document.createElement("div");
  clearDiv.style.clear = "both";
  messagesContainer.appendChild(clearDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
};
//


//Section: Calling the model
const sendMessage = async (message) => {
  addMessage(message, 'user', '/static/images/man.png');
  // Loading animation
  const loadingElement = document.createElement('div');
  const loadingtextElement = document.createElement('p');
  loadingElement.className = `loading-animation`;
  loadingtextElement.className = `loading-text`;
  loadingtextElement.innerText = 'Loading....Please wait';
  messagesContainer.appendChild(loadingElement);
  messagesContainer.appendChild(loadingtextElement);

  async function makePostRequest(msg) {
    try {
      const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: msg })
      });
      return await response.json();
    } catch (error) {
      console.error('Error:', error);
      return { error: 'Could not reach the server. Please try again.' };
    }
  }

  const data = await makePostRequest(message);

  // Deleting the loading animation
  loadingElement.remove();
  loadingtextElement.remove();

  if (data.error) {
    addMessage(data.error, 'error', '/static/images/Error.png');
  } else {
    addMessage(data.response, 'aibot', '/static/images/chat-bot.png');
  }
};
//

//Section: Button to submit to the model and get the response
messageForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (message !== '') {
    messageInput.value = '';
    await sendMessage(message);
  }
});

// Enter sends, Shift+Enter inserts a new line
messageInput.addEventListener('keydown', async (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message !== '') {
      messageInput.value = '';
      await sendMessage(message);
    }
  }
});
