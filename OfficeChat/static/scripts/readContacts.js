
//check for button click and show the message in div and also post to server
const chatForm = document.querySelector('#chatForm');
const sendBtn = document.querySelector('#sendBtn');
const message = document.querySelector('#msg');
const contacts = document.querySelector('.list-group');
const to    = document.querySelector('.chat #to');
const chat_box = document.querySelector('#messages');
const contacturl = '/users';
const chatmessageurl = '/get_chat'
var message_offset = 0;

var queryParams = (params)=>{
    return Object.keys(params).map(function(key) {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
      }).join('&');
} 
document.addEventListener('DOMContentLoaded', () => {
    fetch(contacturl)
        .then((resp) => {
            // console.log(resp);
            //error checking
            //200-299
            if (!resp.ok) throw new Error('was not a valid response');
            return resp.json(); //method to extract JSON string and convert it to an Object
        })
        .then((dataArray) => {
            //console.log(typeof dataArray)
            contact_buttons= `<button type="button" data-contact='${client_id}' class="list-group-item list-group-item-action contact">You </button>`
            contact_buttons+= dataArray.map((contact) => {
                return `<button type="button" data-contact='${contact}' class="list-group-item list-group-item-action contact">${contact} <span id="notify-${contact}" class="badge bg-warning text-dark"></span></button>`
            }).join('');
            contacts.innerHTML=contact_buttons;
            hide();

        })
        .catch((err) => {
            console.warn(err.message);
        });

});

function hide() {
    const contacts = document.querySelectorAll('.contact');
    //console.log(contacts);

    contacts.forEach((contact) => {
        contact.addEventListener('click', (event) => {

            const welcome = document.querySelector('.welcome');
            const chat = document.querySelector('.chat');

            welcome.classList.add('d-none');
            chat.classList.remove('d-none');

            if(to.innerText==event.target.getAttribute('data-contact')){
                return;
            }
            chat_box.innerHTML = '';
            to.innerText = event.target.getAttribute('data-contact');
            loadmessage(to.innerText);
            messages.lastElementChild.scrollIntoView();
            let chatig_person = document.getElementById("notify-"+to.innerText);
            console.log();(chatig_person)
            chatig_person.innerHTML='';

        });
    })
}



async function loadmessage(with_user,offset=0){

    fetch(chatmessageurl+'?'+queryParams({other_person:with_user,offset:offset}))
    .then((resp) =>{
        if (!resp.ok) throw new Error('was not a valid response');
        return resp.json();
    }).then((msgs) =>{
        msgs.forEach(msg=>{
            update_chat_box(msg);
        })
        message_offset+=40;
       
            
    })

}



chat_box.addEventListener('scroll', function() {
    console.log(chat_box.scrollTop,chat_box.clientHeight,chat_box.scrollHeight);
    if ((chat_box.scrollHeight-chat_box.clientHeight) > chat_box.scrollTop+50) {
      scrollUpIcon.classList.add('show');
    } else {
      scrollUpIcon.classList.remove('show');
    }
    if(chat_box.clientHeight>chat_box.scrollTop+10){
        loadmessage(to.innerText,message_offset);
    }
  });

  
  
  