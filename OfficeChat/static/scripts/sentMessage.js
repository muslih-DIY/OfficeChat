


var ws = new WebSocket(`ws://127.0.0.1:8000/chats/`);

sendBtn.addEventListener('click', function(event){
    event.preventDefault();
    
    let msgObject  ={content:message.value,from_:client_id,to:to.innerHTML };
    console.log(JSON.stringify(msgObject));
    ws.send(JSON.stringify(msgObject));
    message.value='';

})

message.addEventListener('keyup', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
    
        let msgObject  ={content:message.value,from_:client_id,to:to.innerHTML };
        console.log(JSON.stringify(msgObject));
        ws.send(JSON.stringify(msgObject));
        message.value='';
    }
  });








