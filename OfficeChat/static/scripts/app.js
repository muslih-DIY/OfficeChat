

var queryParams = (params)=>{
    return Object.keys(params).map(function(key) {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
      }).join('&');
} 



var app = new Vue({
    el: '#app',
    data() {
        return {
            me: {},
            other:{},
            drafted_message: '',
            contacts: [],
            chat: {
            // "group_id": null,
            // "sender_id": 1,
            // "content": "hi",
            // "timestamp": 1690374448.977814,
            // "receiver_id": 1,
            // "message_id": 19,
            // "type": 1,
            // "read": false
            },
        
            connection:null,
        }
    },
    computed: {
        currentChat() {
            if (this.other.id){
                return this.chat[this.other.id]
            }
            
        }
    },
    methods: {
        make_connection(){
            //console.log('starting connection')
            this.connection = new WebSocket('ws://'+window.location.hostname+':'+window.location.port+'/chats/');

            this.connection.onerror = (event) =>{

                //console.log('got error',event);
                this.connection=null;
            }

            this.connection.onopen = (event) =>{
                //console.log('connected');
                 
            } 
            this.connection.onclose = (event) =>{
                //console.log("connection closed");
                this.connection = null;
            }
            this.connection.onmessage = (event) => {

                let message = JSON.parse(event.data);

                this.processMessage(message);
            }
            
        },
        select_other(contact_id) {
            //console.log(contact_id,this.other);
            this.other.id = contact_id;
            let the_other = this.contacts.filter((t) => t.id == contact_id)[0];
            this.other.name = the_other.name;
            this.other.avatarSrc = the_other.avatarSrc;
            this.other.online = the_other.online;

        },
        mark_read_msg(msg_id) {
            //console.log(msg_id, this.other.id);
            let msg = this.chat[this.other.id].filter(t => t.message_id == msg_id)[0];
            msg.read = true;
            //call read update api here and send the message id
            
            let message = {
                type: 3, // READ_ACK
                message_id:msg_id               
            };
            this.connection.send(JSON.stringify(message));

            let currentContact = this.contacts.filter(c => c.id == this.other.id)[0];
            currentContact.notificationCount = Math.max(0, currentContact.notificationCount - 1);
        },
        processMessage(message){
            if(message.type==1){
                // text message
                this.updateNewTextMessage(message);
                return
            }
            if(message.type==3){
                // read acknowledge
                let msg = this.chat[message.receiver_id].filter(t => t.message_id == message.message_id)[0];
                msg.read = true;
                return
            } 
            
            if(message.type==4){
                //online information
                console.log(message.users);
                this.contacts.forEach(contact=>{
                    console.log(contact.id,message.users.includes(contact.id));
                    contact.online = false;
                    if(message.users.includes(contact.id)){
                        contact.online = true;

                    }

                })

            }
        },
        updateNewTextMessage(message) {
            // All the message recived thorugh any mean is handled/stored is here
            let other_person_id =  message.sender_id==this.me.id ? message.receiver_id:message.sender_id;
            if (this.chat[other_person_id] == undefined) {
                this.$set(this.chat, other_person_id, []);
            }

            this.chat[other_person_id].push(message);

            //update notification 
            if (this.me.id==message.receiver_id && this.me.id!=message.sender_id){
            let currentContact = this.contacts.filter(c => c.id == other_person_id)[0];
            currentContact.notificationCount = Math.max(0, currentContact.notificationCount + 1);
            }
            //console.log(this.chat);
        },
        updateOldTextMessage(message) {
            // All the message recived thorugh any mean is handled/stored is here
            let other_person_id =  message.sender_id==this.me.id ? message.receiver_id:message.sender_id;
            if (this.chat[other_person_id] == undefined) {
                this.$set(this.chat, other_person_id, []);
            }

            this.chat[other_person_id].unshift(message);
            // this.chat[other_person_id] = [message ,this.chat[other_person_id] ];
            //console.log(this.chat);
        },        
        send_message() {

            // prepare message and send to the other person through websocket
            let message = {
                type: 1,
                sender_id: this.me.id,
                receiver_id: this.other.id,
                content: this.drafted_message,                
            };
            this.connection.send(JSON.stringify(message));
            this.drafted_message = null;
            //this.processMessage(message);
        },
        async readContacts(){
            //get contacts information using api
            let response = await fetch('/contacts');
            let contactList = await response.json();
            console.log(contactList);
            this.contacts=contactList;
        },

         readChats(contact_id){
            // get the 20 chat of every contacts using api

            //length of chat
            
            let offset = this.chat[contact_id]===undefined ? 0:this.chat[contact_id].length;
            let other_person = this.contacts.filter((t) => t.id == contact_id)[0];
            if(!other_person){
                return;
            }
            if(other_person.message_available!=undefined && other_person.message_available==false)
            {
                return;
            }
            //console.log(queryParams({other_person:contact_id,offset:offset}))

            fetch('/get_chat'+'?'+queryParams({other_person:contact_id,offset:offset}))
            .then((resp) =>{
                if (!resp.ok) throw new Error('was not a valid response');
                return resp.json();
            }).then((msgs) =>{
                
                other_person.message_available=true;
                msgs.forEach(msg=>{
                    this.updateOldTextMessage(msg);                   
                })
                if(msgs.length==0){
                                        
                    other_person.message_available=false;
                }
               
                    
            })

         console.log('chat fething for '+contact_id +' is success'+new Date().toTimeString());   
            
        },
        async scrollChatWindow(){
            
            const chatWindow = document.getElementById('chat-window');
            if(chatWindow.scrollTop==0){
                this.readChats(this.other.id);
                let secondChild = chatWindow.querySelectorAll('li')[1];
                secondChild.scrollIntoView({ behavior: 'smooth' });
            }
            
        },
        async readMydDetails(){

            let response = await fetch('me');
            let aboutMe = await response.json();
            this.me = {
                id: aboutMe.id,
                name: aboutMe.name,
                avatarSrc: aboutMe.profile_picture,
                online:true
            };
            this.other = {
                id: aboutMe.id,
                name: aboutMe.name,
                avatarSrc: aboutMe.profile_picture,
                online:true
            };
        },
        handleImagePaste(event) {
            const items = event.clipboardData.items;
            for (let i = 0; i < items.length; i++) {
                const item = items[i];
                if (item.type.indexOf('image') === 0) {
                    const blob = item.getAsFile();
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.imageData = e.target.result;
                    };
                    reader.readAsDataURL(blob);
                }
            }
        }
    },
    async mounted() {
        
        await this.readMydDetails();
        await this.readContacts();
        this.make_connection();
        this.contacts.forEach(c=>{
            if (c.id==this.me.id){
                c.online =true;
            }
            this.readChats(c.id);
        })
        
    },

});
