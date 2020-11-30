import {base_url} from './questionanswers.js';
// Gets all submit events of the entire signup html page

document.body.addEventListener('submit', submitSignupData);

// A class that has signin functions


class SignupFunctions{

    // A function to submit signup data
    static submitSignupData(e){

        // Grabs signup form data to be sent to the server by an ajax request
        let signupform = e.target;
        let signupData = new FormData(signupform);

        // initialises ajax object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('POST', `${base_url}/signup`);

        // response from the server
        xhr.onload = function(onloadevent) {
            // user registered successfully
            if(xhr.status == 201){
                // redirects to login page
                window.location.href = `signin`;
            }
            else{

                // response error from the server
                let error = JSON.parse(xhr.responseText);

                // Gets error container
                let signupErrorContainer = e.target.previousElementSibling;

                // Accesses the list tag to display the error
                let signupErrorTag = signupErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(signupErrorTag.innerHTML == ''){
                    signupErrorTag.innerHTML = error.error;
                }
                else{
                    // If list tag has an error text replace it with a new one
                    signupErrorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                signupErrorContainer.style.display = 'block';

                // Makes the error message disappear in 4 seconds
                // and sets the value of the list tag to an empty text.
                setTimeout(function(){
                    signupErrorTag.innerHTML = '';
                    signupErrorContainer.style.display = 'none';
                }
                ,4000)
            }
        };

        // sends the signup data
        xhr.send(signupData);

    }
}


// Submit function

function submitSignupData(e){

    // Event that submits login data
    if(e.target.id === 'signup-form'){
        e.preventDefault();
        SignupFunctions.submitSignupData(e);
    }

}