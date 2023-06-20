//check for button click and show the message in div and also post to server
const chatForm = document.querySelector('#chatForm');
const messageInput = document.querySelector('#msg');

chatForm.addEventListener('submit', function(event){
    event.preventDefault();
    const messages = document.querySelector('#messages');
    const sentMessage = document.createElement('p');

    
    const message = messageInput.value.trim();
    messageInput.select();

    //sentMessage.textContent = message;

    // Get and clone our template
    let template = document.getElementById('message');
    let clone = template.content.cloneNode(true);

    // Update our cloned template
    clone.querySelector('.user').innerText = "admin";
    clone.querySelector('.message').innerText = message;
    clone.querySelector('.datetime').innerText = new Date().toLocaleString();
    

    

    messages.appendChild(clone);
    messages.scrollTop = messages.scrollHeight;
});










