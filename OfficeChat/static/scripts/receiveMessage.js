ws.onmessage = function (event) {
    //var messages = document.getElementById('messages')
    // var message = document.createElement('li')
    // // var content = document.createTextNode(event.data)
    let data = JSON.parse(event.data);
    console.log(data);


    const messages = document.querySelector('#messages');
    //const receivedMessage = document.createElement('p');


    //const message = messageInput.value.trim();
    //messageInput.select();

    //sentMessage.textContent = message;

    //Get and clone our template
    console.log(client_id);
    console.log(data.from_);
    if (client_id === data.from_) {
        let template = document.getElementById('message-send');
        let clone = template.content.cloneNode(true);

        //Update our cloned template
        clone.querySelector('.user').innerText = data.from_;
        clone.querySelector('.message').innerText = data.content;
        clone.querySelector('.datetime').innerText = data.at;
        messages.appendChild(clone);
    }else{
        let template = document.getElementById('message-receive');
        let clone = template.content.cloneNode(true);

        //Update our cloned template
        clone.querySelector('.user').innerText = data.from_;
        clone.querySelector('.message').innerText = data.content;
        clone.querySelector('.datetime').innerText =  new Date(data.at).toLocaleTimeString();;
        messages.appendChild(clone);
    }

    //messages.scrollTop = messages.scrollHeight;




    // /// data preparation
    // var div = document.createElement('div');
    // var from_head = document.createTextNode(data.from_);
    // var msg = document.createTextNode(data.content);
    // var time = document.createTextNode(data.at);
    // let span_div = document.createElement('div');
    // let span = document.createElement('span');

    // span.innerText = data.from_ + ' ';     
    // span_div.appendChild(span);
    // span = document.createElement('span');                
    // span.innerText = new Date(data.at).toLocaleTimeString();
    // span_div.appendChild(span);

    // let msg_div = document.createElement('div');
    // msg_div.innerText = data.content;

    // div.appendChild(span_div);
    // div.appendChild(msg_div);                            

    // message.appendChild(div)
    // messages.appendChild(message)
};
