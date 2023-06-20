const url = 'https://jsonplaceholder.typicode.com/users';

document.addEventListener('DOMContentLoaded', () => {
    fetch(url)
        .then((resp) => {
            // console.log(resp);
            //error checking
            //200-299
            if (!resp.ok) throw new Error('was not a valid response');
            return resp.json(); //method to extract JSON string and convert it to an Object
        })
        .then((dataArray) => {
            const contacts = document.querySelector('.list-group');
            //console.log(typeof dataArray)
            contacts.innerHTML = dataArray.map((contact) => {
                return `<button type="button" class="list-group-item list-group-item-action contact">${contact.name}</button>`
            }).join('');
            hide();

        })
        .catch((err) => {
            console.warn(err.message);
        });

});

function hide() {
    const contacts = document.querySelectorAll('.contact');
    console.log(contacts);

    contacts.forEach((contact) => {
        contact.addEventListener('click', (event) => {
            console.log(event)
            //select a div which contains welcome message and hide it
            const welcome = document.querySelector('.welcome');
            const chat = document.querySelector('.chat');
            console.log(event.target.innerHTML);

            //
            welcome.classList.add('d-none');
            chat.classList.remove('d-none');

        });
    })
}


