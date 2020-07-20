// Gets all submit events of the entire login html page

document.body.addEventListener('submit', submitLoginData);

// A class that has login functions


class LoginFunctions{

    // A function to submit signin data
    static submitSigninData(e){
        // Gets form's login data
        let loginform = e.target;
        let loginData = new FormData(loginform);
        console.log(loginData);
        // Initialise XMLHttpRequest
        let xhr = new XMLHttpRequest()
        xhr.open("POST", "http://127.0.0.1:5000/signin", true);
        // Open the request
        xhr.onload = function(onloadevent) {
            if (xhr.status == 200) {
              const response = JSON.parse(this.responseText);
              console.log(response);
            }
            else if (xhr.status == 401) {
                const response = JSON.parse(this.responseText);
                console.log(response);
              } 
            else {
                const loginFailedResponse = JSON.parse(this.responseText);
                console.log(loginFailedResponse);
            }
          };
        
        xhr.send(loginData);
        // Gets error login container
        // let loginErrorContainer = e.target.previousElementSibling;

        // Accesses the list tag to display the error
        // let loginErrorTag = loginErrorContainer.children[0];

        // if the list tag doesn't contain an error message,
        // add one.
        // if(loginErrorTag.innerHTML == ''){
            
        //     loginErrorTag.innerHTML = "Please provide correct username and password";
        // }
        // else{
        //     // If list tag has an error text replace it with a new one
        //     loginErrorTag.innerHTML = "Please fill all values to login";
        // }

        // Display the error container, to display the error,
        // message.
        // loginErrorContainer.style.display = 'block';

        // Makes the error message disappear in 30 seconds
        // and sets the value of the list tag to an empty text.
        // setTimeout(function(){
        //     loginErrorTag.innerHTML = '';
        //     loginErrorContainer.style.display = 'none';
        // }
        // ,30000)

    }
}


// Submit function

function submitLoginData(e){
    
    // Event that submits login data
    if(e.target.id === 'login-form'){
        e.preventDefault();
        LoginFunctions.submitSigninData(e);
    }

}