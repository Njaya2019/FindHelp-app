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

        // Gets error login container
        let newPasswordErrorContainer = e.target.previousElementSibling;

        // Accesses the list tag to display the error
        let newPasswordErrorTag = newPasswordErrorContainer.children[0];

        // if the list tag doesn't contain an error message,
        // add one.
        if(newPasswordErrorTag.innerHTML == ''){
            newPasswordErrorTag.innerHTML = "Please provide a valid email";
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
        }
        ,30000)

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