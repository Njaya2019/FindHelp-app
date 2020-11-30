import {base_url} from './questionanswers.js';
// Gets all submit events of the entire login html page

document.body.addEventListener('submit', submitLoginData);

// A class that has login functions
class LoginFunctions{

    // A function to submit signin data
    static submitSigninData(e){

        // Gets form's login data
        let loginform = e.target;
        let loginData = new FormData(loginform);

        // Initialise XMLHttpRequest
        let xhr = new XMLHttpRequest()

        // Opens the request
        xhr.open("POST", `${base_url}/signin`, true);
        
        xhr.onload = function(onloadevent) {

            if (xhr.status == 200) {
            
              // Login was successful
              const response = JSON.parse(this.responseText);

              localStorage.setItem('token', response.token);
              window.location.href = `questions/`;
            }
            else {

              // Login failed
              const loginFailedResponse = JSON.parse(this.responseText);

              // Gets error login container
              let loginErrorContainer = e.target.previousElementSibling;

              // Accesses the list tag to display the error
              let loginErrorTag = loginErrorContainer.children[0];

              // if the list tag doesn't contain an error message,
              // add one.
              if(loginErrorTag.innerHTML == ''){
                  
                  loginErrorTag.innerHTML = loginFailedResponse.error;
              }
              else{

                  // If list tag has an error text replace it with a new one
                  loginErrorTag.innerHTML = loginFailedResponse.error;
              }

              // Display the error container, to display the error,
              // message.
              loginErrorContainer.style.display = 'block';

              // Makes the error message disappear in 30 seconds
              // and sets the value of the list tag to an empty text.
              setTimeout(function(){
                  loginErrorTag.innerHTML = '';
                  loginErrorContainer.style.display = 'none';
              }
              ,9000)
            }
          };
        
        xhr.send(loginData);

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
