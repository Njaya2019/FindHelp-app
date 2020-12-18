// import {base_url}  from './questionanswers.js';
let base_url = window.location.origin;

// gets the URL search string, that is the path
let currentLocation = window.location.pathname;

// puts the url values in an array
let urlArray = currentLocation.split('/', 3);

// grabs the token, the last element at index 2
let token = urlArray[2];

// Listens to a submit event
// document.body.addEventListener("submit", submitEvent);

// function submitEvent(e){
//     // prevent default form submit on 'enter' keypress.
//     e.preventDefault();
// }

// Listens to a keyboard press
document.body.addEventListener("keypress", keyEvent);

function keyEvent(e){
    // Enter key pressed when in password textbox to focus on the next element
    if(e.target.id == "password" && e.keyCode == 13){
        e.target.nextElementSibling.focus();
    }
    // Enter key pressed while in confirm password textbox to focus on the next element
    else if(e.target.id === "confirmpassword" && e.keyCode === 13){
        e.target.nextElementSibling.focus();
    }
    // if in confirm button textbox and presses the back space key
    else if(e.target.id === "confirmpassword" && e.keyCode === 8){
        e.target.previousElementSibling.focus();
    }
    else{
        console.log('Nothing');
    }
}


// Gets all submit events of the entire html page

document.body.addEventListener('submit', submitNewPassword);

// A class that has reset functions


class NewPasswordFunctions{

    // A function to submit signin data
    static submitPassword(e){

        // gets password form data
        let passwordData = new FormData(e.target);

        // instantiates xml http request object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('POST', `${base_url}/resetpassword/${token}`);

        // Loads the response from the server
        xhr.onload = function(loadevent){
            // successfully updated the password
            if(xhr.status == 200){
                let message = JSON.parse(xhr.responseText);
                // Displays a message the password has been successfully changed
                e.target.parentNode.innerHTML = message.message;
            }
            else{
                // Failed updating the password

                // gets the error message
                let error = JSON.parse(xhr.responseText);
                
                // Gets error login container
                let newPasswordErrorContainer = e.target.previousElementSibling;

                // Accesses the list tag to display the error
                let newPasswordErrorTag = newPasswordErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(newPasswordErrorTag.innerHTML == ''){
                    newPasswordErrorTag.innerHTML = error.error;
                }
                else{
                    // If list tag has an error text replace it with a new one
                    newPasswordErrorTag.innerHTML = "Please fill all values";
                }

                // Display the error container, to display the error,
                // message.
                newPasswordErrorContainer.style.display = 'block';

                // Makes the error message disappear in 30 seconds
                // and sets the value of the list tag to an empty text.
                setTimeout(function(){
                    newPasswordErrorTag.innerHTML = '';
                    newPasswordErrorContainer.style.display = 'none';
                },4000);
            }
        };

        xhr.send(passwordData);
    }
}


// Submit function

function submitNewPassword(e){

    // Event that submits new password
    if(e.target.id === 'password-form'){
        e.preventDefault();
        NewPasswordFunctions.submitPassword(e);
    }

}