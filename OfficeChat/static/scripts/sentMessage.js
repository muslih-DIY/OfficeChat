//check for button click and show the message in div and also post to server
const chatForm = document.querySelector('#chatForm');
const sendBtn = document.querySelector('#sendBtn');
const message = document.querySelector('#msg');




var ws = new WebSocket(`ws://127.0.0.1:8000/chats/`);

sendBtn.addEventListener('click', function(event){
    event.preventDefault();
    const to = document.querySelector('#to');
    let msgObject  ={content:message.value,from_:client_id,to:to.innerHTML };
    console.log(JSON.stringify(msgObject));
    ws.send(JSON.stringify(msgObject));





    //const messages = document.querySelector('#messages');
    //const sentMessage = document.createElement('p');

    
    //const message = messageInput.value.trim();
    //messageInput.select();

    //sentMessage.textContent = message;

    // Get and clone our template
    //const template = document.getElementById('message-send');
    //const clone = template.content.cloneNode(true);

    // Update our cloned template
    //clone.querySelector('.user').innerText = "admin";
    //clone.querySelector('.message').innerText = message;
    //clone.querySelector('.datetime').innerText = new Date().toLocaleString();
    

    

    //messages.appendChild(clone);
    //messages.scrollTop = messages.scrollHeight;
});









