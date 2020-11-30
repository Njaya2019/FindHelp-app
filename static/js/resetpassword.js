// import {base_url} from './questionanswers.js';
let base_url = window.location.origin;
// Gets all submit events of the entire html page

document.body.addEventListener('submit', submitEmail);

// A class that has recovery functions


class ResestPasswordFunctions{

    // A function to submit email
    static submitEmailData(e){

        // Grabs email form data to be sent to the server by an ajax request
        let emailform = e.target;
        let emailData = new FormData(emailform);

        // initialise ajax request object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('POST', 'http://127.0.0.1:5000/resetpassword');

        // response from the server
        xhr.onload = function(onload){

            // sets the user name
            if(xhr.status === 200){

                reset_message = JSON.parse(this.responseText);

                form_parent_container = e.target.parentNode;

                form_parent_container.innerHTML = reset_message.message
            }
            else{
                // error response
                let error = JSON.parse(this.responseText);
                // Gets error container
                let resesetErrorContainer = e.target.previousElementSibling;

                // Accesses the list tag to display the error
                let resesetErrorTag = resesetErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(resesetErrorTag.innerHTML == ''){
                    resesetErrorTag.innerHTML = error.error;
                }
                else{
                    // If list tag has an error text replace it with a new one
                    resesetErrorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                resesetErrorContainer.style.display = 'block';

                // Makes the error message disappear in 30 seconds
                // and sets the value of the list tag to an empty text.
                setTimeout(function(){
                    resesetErrorTag.innerHTML = '';
                    resesetErrorContainer.style.display = 'none';
                }
                ,3000);
            }
        }

        // sends the request
        xhr.send(emailData);

    }
}


// Submit function

function submitEmail(e){

    // Event that submits login data
    if(e.target.id === 'reset-form'){
        e.preventDefault();

        // ResestPasswordFunctions.submitEmailData(e);

        function makeRequest(){

            return new Promise(function (resolve, reject) {
                let emailform = e.target;
                let emailData = new FormData(emailform);
                let xhr = new XMLHttpRequest();
                xhr.open('POST', `${base_url}/resetpassword`);
                xhr.onload = function () {
                    if (this.status >= 200 && this.status < 300) {
                        console.log('instructions were sent');
                        resolve(JSON.parse(xhr.responseText));
                    } else {
                        reject(JSON.parse(xhr.responseText));
                    }
                };
                xhr.onerror = function () {
                    reject(JSON.parse(xhr.responseText));
                };
                xhr.send(emailData);
            }).then(function(result){
                console.log(result);
            }).catch(function(result){
                // error response
                let error = result;
                // Gets error container
                let resesetErrorContainer = e.target.previousElementSibling;

                // Accesses the list tag to display the error
                let resesetErrorTag = resesetErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(resesetErrorTag.innerHTML == ''){
                    resesetErrorTag.innerHTML = error.error;
                }
                else{
                    // If list tag has an error text replace it with a new one
                    resesetErrorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                resesetErrorContainer.style.display = 'block';

                // Makes the error message disappear in 30 seconds
                // and sets the value of the list tag to an empty text.
                setTimeout(function(){
                    resesetErrorTag.innerHTML = '';
                    resesetErrorContainer.style.display = 'none';
                }
                ,3000);
            });
        } 
        // makeRequest.then(function(result){
        //     console.log(result);
        // }).catch(function(result){
        //     console.log(result);
        // });

        
        async function sendEmail(){

            await makeRequest();

            
        }

        sendEmail();
    }
}