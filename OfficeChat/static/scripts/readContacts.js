
//check for button click and show the message in div and also post to server
const chatForm = document.querySelector('#chatForm');
const sendBtn = document.querySelector('#sendBtn');
const message = document.querySelector('#msg');
const contacts = document.querySelector('.list-group');
const to    = document.querySelector('.chat #to');
const to_icon    = document.querySelector('.chat #to-icon');
const messages = document.querySelector('#messages');
const contacturl = '/users';
const chatmessageurl = '/get_chat'
var message_offset = 0;
var message_available = true;

const randomColors = (colorArray) => {
    const randomIndex = Math.floor((Math.random()+Math.random())/2 * colorArray.length);
    return colorArray[randomIndex];
  };
  
  // only these colors are allowed
  const colors = [
    'bg-primary text-white', 'bg-success text-white', 'bg-danger text-white', 'bg-dark text-white',
    'bg-danger text-black' ,
];


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
            contact_buttons= `<div class="d-flex bg-white align-items-center"><div class='i-circle align-middle p-1 bg bg-primary text-white'>Me</div><button type="button" data-contact='${client_id}' class="list-group-item list-group-item-action contact">Me</button></div>`
            contact_buttons+= dataArray.map((contact) => {
                return `<div class="d-flex bg-white align-items-center"><div class='i-circle align-middle p-1 ${randomColors(colors)}'>${contact[0].toUpperCase()}</div><div class="w-100"><button type="button" data-contact='${contact}' class="list-group-item list-group-item-action contact">${contact}</button></div><div><span id="notify-${contact}" class="badge bg-warning text-dark"></span></div></div>`
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

            messages.innerHTML = '';
            to.innerText = event.target.getAttribute('data-contact');
            to_icon.innerText = to.innerText[0].toUpperCase();
            message_offset = 0;
            message_available = true ;
            fetch(chatmessageurl+'?'+queryParams({other_person:to.innerText,offset:0}))
            .then((resp) =>{
                if (!resp.ok) throw new Error('was not a valid response');
                return resp.json();
            })
            .then((msgs) =>{
                msgs.forEach(msg=>{
                    update_chat_box(msg,false);
                })
            })
            .then(() =>{

                // messages.lastElementChild.scrollIntoView();
                let chatig_person = document.getElementById("notify-"+to.innerText.toLowerCase());
                chatig_person.innerHTML='';
                let allmessage = messages.querySelectorAll('#messages div.message');
                let lastmessage = allmessage[allmessage.length- 1];
                message_offset+=10;
            })



        });
    })
}



async function loadmessage(with_user,offset=0){
    
    // if message is not message_available not load
    if(!message_available){
        return;
    }

    fetch(chatmessageurl+'?'+queryParams({other_person:with_user,offset:offset}))
    .then((resp) =>{
        if (!resp.ok) throw new Error('was not a valid response');
        return resp.json();
    }).then((msgs) =>{
        msgs.forEach(msg=>{
            update_chat_box(msg,false);
        })
        if(msgs.length!=0){
            message_offset+=10;
            
        }
        else{
            message_available = false;
        }
       
            
    })

}


messages.addEventListener('scroll', function() {
    console.log(messages.scrollTop,messages.clientHeight,messages.scrollHeight);
    if ((messages.scrollHeight-messages.clientHeight) > messages.scrollTop+50) {
      scrollUpIcon.classList.add('show');
    } else {
      scrollUpIcon.classList.remove('show');
    }
    if(messages.scrollTop==0){
        loadmessage(to.innerText,message_offset);
    }
    if((messages.scrollTop+messages.clientHeight)+4>messages.scrollHeight){
        let chatig_person = document.getElementById("notify-"+to.innerText);
        chatig_person.innerHTML='';
    }
  });

  
  
  