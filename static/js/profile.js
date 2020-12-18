let sidebar_buttons = document.querySelectorAll('.sidebar-button');
let updateProfile = document.getElementById("update-div");
let profileInformation = document.getElementById("profile-div");
let questions = document.getElementById("questions-div");


for(i=0; i<sidebar_buttons.length; i++){
    sidebar_buttons[i].addEventListener('click', function(){

        currentActiveSidebarButton = document.querySelectorAll('.active');

        currentActiveSidebarButton[0].className = currentActiveSidebarButton[0].className.replace("active", "");

        this.className += " active";
        
        if(this.id === 'questions'){
            displayContent.hideContents(updateProfile, profileInformation);
            displayContent.displayContents(questions);
        }
        else if(this.id === 'update'){
            displayContent.hideContents(questions, profileInformation);
            displayContent.displayContents(updateProfile);
            display_populate_update_form(updateProfile);      
        }
        else{
            displayContent.hideContents(questions, updateProfile);
            displayContent.displayContents(profileInformation);
            display_user_info(profileInformation);
            display_user_status(profileInformation);    
        }
    });

}

class displayContent{

    static displayContents(){
        for(i=0; i<arguments.length; i++){
            arguments[i].style.display = 'block';
        }
    }

    static hideContents(){
        for(i=0; i<arguments.length; i++){
            arguments[i].style.display = 'none';
        }
    }
}

// ====================================
// FUNCTION TO DISPLAY USER INFORMATION
//=====================================
let base_url = window.location.origin;

function display_user_info(element){

    //intialise xmlhttprequest object
    let xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('POST', `${base_url}/questions/`);

    // Response from the server
    xhr.onload = function(onload_event){

        if(xhr.status == 200){

            // request was successfull
            let profile_info = JSON.parse(xhr.responseText);

            // displays the fullname
            element.children[0].children[2].children[0].children[1].innerHTML =  profile_info.fullname;

            // displays the email
            element.children[0].children[2].children[0].children[3].innerHTML =  profile_info.email;

            // displays the role
            element.children[0].children[2].children[0].children[5].innerHTML =  profile_info.role?'Moderate user':'user';

        }
        else{

            // request was unsuccessfull

        }
    };

    // sends the request
    xhr.send();

}


// ===========================================
// FUNCTION TO DISPLAY USER's ACTIVITY REPORT
//============================================

function display_user_status(element){

    // Starts the loader
    element.parentNode.nextElementSibling.style.display = 'block';

    //intialise xmlhttprequest object
    let xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('GET', `${base_url}/users/status`);

    // Response from the server
    xhr.onload = function(onload_event){

        if(xhr.status == 200){

            // hides the loader
            element.parentNode.nextElementSibling.style.display = 'none';

            // request was successfull
            let profile_status = JSON.parse(xhr.responseText);

            // displays the number of questions
            element.children[0].children[4].children[0].children[1].innerHTML =  profile_status.report.questions;

            // displays the number of answers
            element.children[0].children[4].children[0].children[3].innerHTML =  profile_status.report.answers;

            // displays the number of correct answers
            element.children[0].children[4].children[0].children[5].innerHTML =  profile_status.report.correct_answers;

        }
        else{

            // request was unsuccessfull

            // hides the loader
            element.parentNode.nextElementSibling.style.display = 'none';

        }

    };

    // sends the request
    xhr.send();

}

// =========================================================
// FUNCTION TO POPULATE USER INFORMATION ON THE UPDATE FORM
//==========================================================

function display_populate_update_form(element){

    // Starts the loader
    element.parentNode.nextElementSibling.style.display = 'block';

    //intialise xmlhttprequest object
    let xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('POST', `${base_url}/questions/`);

    // Response from the server
    xhr.onload = function(onload_event){

        if(xhr.status == 200){

            // hides the loader
            element.parentNode.nextElementSibling.style.display = 'none';

            // request was successfull
            let profile_info = JSON.parse(xhr.responseText);

            // displays the fullname
            element.children[1].children[2].children[1].children[1].value =  profile_info.fullname;

            // displays the email
            element.children[1].children[2].children[1].children[3].value  =  profile_info.email;

            // displays the role
            // This specifies the value to be selected in the option dropdown list
            element.children[1].children[2].children[1].children[5].value =  profile_info.role?'true':'false';

        }
        else{

            // request was unsuccessfull

            // hides the loader
            element.parentNode.nextElementSibling.style.display = 'none';

        }
    };

    // sends the request
    xhr.send();

}

// ==============================================
// FUNCTIONALITY TO UPDATE THE USER INFORMATION
//===============================================

document.getElementById('update-form').addEventListener('submit', updateUserInfo);

function updateUserInfo(e){

    // prevent form default action
    e.preventDefault();

    // the update form
    let update_form = e.target;

    // Shows the loader
    update_form.parentNode.parentNode.parentNode.parentNode.nextElementSibling.style.display = 'block';

    // gets the form data
    let updateFormData = new FormData(e.target);

    //intialise xmlhttprequest object
    let xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('PUT', `${base_url}/users/edit`);
    
        // Response from the server
        xhr.onload = function(onload_event){
    
        if(xhr.status == 200){

            // Hides the loader
            update_form.parentNode.parentNode.parentNode.parentNode.nextElementSibling.style.display = 'none';
    
            // request was successfull
            let updated_user = JSON.parse(xhr.responseText);

            // Displays the updated infromation on the form

            // displays the fullname
            update_form.children[1].value =  updated_user.updated_user.fullname;

            // displays the email
            update_form.children[3].value  =  updated_user.updated_user.email;

            // displays the role
            // This specifies the value to be selected in the option dropdown list
            update_form.children[5].value =  updated_user.updated_user.role?'true':'false';

            // success div
            let successDiv = e.target.previousElementSibling;

            // displays the success container
            successDiv.style.display = 'block';

            // places the success message to the container
            successDiv.innerHTML = 'The information was successfully updated';

            // Changes the text color to blue
            successDiv.style.color = 'blue';
            
            // makes the error disappear in 3 seconds
            setTimeout(function(){
            
                // clears the success message in the error container
                successDiv.innerHTML = '';

                // Changes the text color back to red
                successDiv.style.color = 'red';
            
                // hides the success container
                successDiv.style.display = 'none';

            }, 3000);
            
        }
        else{

            // Hides the loader
            update_form.parentNode.parentNode.parentNode.parentNode.nextElementSibling.style.display = 'none';
    
            // request was unsuccessfull
            let error = JSON.parse(xhr.responseText);

            // gets the error container
            let errorDiv = e.target.previousElementSibling;
            
            // displays the error container
            errorDiv.style.display = 'block';

            // places the error message to the container
            errorDiv.innerHTML = error.error;

            // makes the error disappear in 3 seconds
            setTimeout(function(){

                // clears the error message in the error container
                errorDiv.innerHTML = '';

                // hides the error container
                errorDiv.style.display = 'none';

            }, 3000);
    
        }
    };
    
    // sends the request
    xhr.send(updateFormData);
}