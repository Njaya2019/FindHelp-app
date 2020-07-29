// Gets all submit events of the entire html page

document.body.addEventListener('submit', submitEmail);

// A class that has recovery functions


class ResestPasswordFunctions{

    // A function to submit email
    static submitEmailData(e){

        // Gets error container
        let resesetErrorContainer = e.target.previousElementSibling;

        // Accesses the list tag to display the error
        let resesetErrorTag = resesetErrorContainer.children[0];

        // if the list tag doesn't contain an error message,
        // add one.
        if(resesetErrorTag.innerHTML == ''){
            resesetErrorTag.innerHTML = "Please provide a valid email";
        }
        else{
            // If list tag has an error text replace it with a new one
            resesetErrorTag.innerHTML = "Please provide an email";
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
        ,30000)

    }
}


// Submit function

function submitEmail(e){

    // Event that submits login data
    if(e.target.id === 'reset-form'){
        e.preventDefault();
        ResestPasswordFunctions.submitEmailData(e);
    }

}