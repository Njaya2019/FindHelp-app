// Gets all submit events of the entire signup html page

document.body.addEventListener('submit', submitSignupData);

// A class that has signin functions


class SignupFunctions{

    // A function to submit signup data
    static submitSignupData(e){

        // Gets error container
        let signupErrorContainer = e.target.previousElementSibling;

        // Accesses the list tag to display the error
        let signupErrorTag = signupErrorContainer.children[0];

        // if the list tag doesn't contain an error message,
        // add one.
        if(signupErrorTag.innerHTML == ''){
            signupErrorTag.innerHTML = "Please provide valid values for all fields";
        }
        else{
            // If list tag has an error text replace it with a new one
            signupErrorTag.innerHTML = "Please fill all fields to register";
        }

        // Display the error container, to display the error,
        // message.
        signupErrorContainer.style.display = 'block';

        // Makes the error message disappear in 30 seconds
        // and sets the value of the list tag to an empty text.
        setTimeout(function(){
            signupErrorTag.innerHTML = '';
            signupErrorContainer.style.display = 'none';
        }
        ,30000)

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