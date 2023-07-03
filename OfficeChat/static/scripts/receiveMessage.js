

ws.onmessage = function (event) {
    //var messages = document.getElementById('messages')
    // var message = document.createElement('li')
    // // var content = document.createTextNode(event.data)
    let data = JSON.parse(event.data);
    update_chat_box(data);
    console.log(data);
    if (client_id != data.from_) {
        let chatig_person = document.getElementById("notify-"+data.from_);
        let count = chatig_person.innerHTML;
        console.log(chatig_person,count);
        if (!count){
            chatig_person.innerHTML='1';         
            return;                
        }
        chatig_person.innerHTML = parseInt(count) +1;
            
    }

};


function update_chat_box(msg){
    //Get and clone our template

    if(msg.from_==to.innerHTML || msg.to==to.innerHTML){

        
        if (client_id === msg.from_) {
            let template = document.getElementById('message-send');
            let clone = template.content.cloneNode(true);

            //Update our cloned template
            // clone.querySelector('.user').innerText = msg.from_;
            clone.querySelector('.message').innerText = msg.content;
            clone.querySelector('.datetime').innerText = new Date(msg.at).toLocaleString();
            messages.appendChild(clone);
            messages.lastElementChild.scrollIntoView();
        }else{
            let template = document.getElementById('message-receive');
            let clone = template.content.cloneNode(true);

            //Update our cloned template
            clone.querySelector('.user').innerText = msg.from_;
            clone.querySelector('.message').innerText = msg.content;
            clone.querySelector('.datetime').innerText = new Date(msg.at).toLocaleString();
            messages.appendChild(clone);
            
        }
        
    }
}