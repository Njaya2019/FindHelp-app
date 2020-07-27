document.body.addEventListener('click', clickActions);

// Gets the confirming delete parent element
let confirmDeleteWindow = '';

function clickActions(e){
    if(e.target.classList.contains('three-dots')){
        // Displays actions on a question.
        if(e.target.nextElementSibling.style.display == 'flex'){
            e.target.nextElementSibling.style.display = 'none';
        }
        else{
            e.target.nextElementSibling.style.display = 'flex';
        }
    }
    else if(e.target.classList.contains('delete-question')){
        // Deleting question action option clicked.
        // Displays confirming delete window.
        confirmDeleteWindow = e.target.parentNode.parentNode.parentNode.parentNode.children[4];
        confirmDeleteWindow.style.display = 'block';
        e.target.parentNode.style.display = 'none';
    }          
    else if(e.target.classList.contains('confirm-question-delete-background')){
        // closes confirming delete window, if it's outer window is clicked.
        // cancels confirming delete window.
        confirmDeleteWindow.style.display = 'none';
    }
    else if(e.target.classList.contains('delete-question-cancel')){
        // closes confirming delete window using cancel button.
        // cancels confirming delete widow.
        confirmDeleteWindow = e.target.parentNode.parentNode.parentNode;
        confirmDeleteWindow.style.display = 'none';
    }
    else if(e.target.classList.contains('edit-question')){
        // Editing question option clicked.
        // displays the editing form.

        // gets title and description values of the question for editing.
        let editQuestionTitle =  e.target.parentNode.parentNode.parentNode.parentNode.children[1].children[0].innerHTML;
        let editQuestionDescription =  e.target.parentNode.parentNode.parentNode.parentNode.children[1].children[1].innerHTML;

        // Hides the options window after the edit event.
        e.target.parentNode.style.display = "none";

        // Hides the posted question.
        e.target.parentNode.parentNode.parentNode.parentNode.children[1].style.maxHeight = 0 + "px";

        // Gets the form that would facilitate the editing of the question.
        let editQuestionFormElement = e.target.parentNode.parentNode.parentNode.parentNode.children[3].children[0];

        // Supplies the original posted text to the input and textarea elements of form for editing the question.
        editQuestionFormElement.children[0].value = editQuestionTitle;
        editQuestionFormElement.children[1].value = editQuestionDescription;
        
        // if the form is already open, closes it and places back the posted question.
        if(editQuestionFormElement.style.maxHeight == editQuestionFormElement.scrollHeight + "px"){
            editQuestionFormElement.style.maxHeight = 0 + "px";
            e.target.parentNode.parentNode.parentNode.parentNode.children[1].style.maxHeight = e.target.parentNode.parentNode.parentNode.parentNode.children[1].scrollHeight + "px";
        }
        else{
            // Else display the editing question form.
            editQuestionFormElement.style.maxHeight = editQuestionFormElement.scrollHeight + "px";
        }
    }
    else if(e.target.classList.contains('cancel-button')){
        // Closes the editing question form.
        e.target.parentNode.parentNode.parentNode.parentNode.children[3].children[0].style.maxHeight = null;
        e.target.parentNode.parentNode.parentNode.parentNode.children[1].style.maxHeight = e.target.parentNode.parentNode.parentNode.parentNode.children[1].scrollHeight + "px";  
    }
    // Upload question image container clicked
    else if(e.target.id == 'question-image'){
        // uploads the image and displays its name on the button.
        let labelTag = e.target.nextElementSibling;
        e.target.addEventListener('change', function(event){
            // splits the string with a back slash and returns the last element
            // of the array which is the image's name.
            let imageName = event.target.value.split("\\").pop();
            if (imageName){
                labelTag.innerHTML = imageName;
            }
        });
    }
    else{

    }

}


// Gets the question's form id 
submitQuestion = document.querySelector("#post-question-form");

// A submit event to post a question
submitQuestion.addEventListener('submit', postQuestion);

// A function to run on submit question event
function postQuestion(e){

    // Prvents action of the form from routing automatically
    e.preventDefault();

    // Grabs form data to be sent to the server by an ajax request
    let questionform = e.target;
    let questionData = new FormData(questionform);

    // initialise ajax request
    let xhr = new XMLHttpRequest();

    // open the request
    xhr.open('POST', 'http://127.0.0.1:5000/questions', true);

    // What should happen if the reponse received from the server
    xhr.onload = function(onloadevent){

        // successful posted question
        if (xhr.status == 201){

            get_questions();

            // resets form data
            questionform.reset();
        }
        else{
            // Response error from the server
            let error = JSON.parse(xhr.responseText);

            // Gets the error div container
            let questionErrorContainer = e.target.parentNode.previousElementSibling;

            // Accesses the list tag to display the error
            let questionErrorTag = questionErrorContainer.children[0];

            // if the list tag doesn't contain an error message,
            // add one.
            if(questionErrorTag.innerHTML == ''){

                questionErrorTag.innerHTML = error.error;
            }
            else{

                // If list tag has an error text replace it with a new one
                questionErrorTag.innerHTML = error.error;
            }

            // Display the error container, to display the error,
            // message.
            questionErrorContainer.style.maxHeight = questionErrorContainer.scrollHeight + 'px';

            // Deletes all list error tags after 30 seconds
            setTimeout(function(){

                // Replace the current error text with an empty string
                questionErrorTag.innerHTML = '';

                // Makes the error container to disappear
                questionErrorContainer.style.maxHeight = 0 + 'px';

            }, 30000);      
        }
    };

    // Sends the request
    xhr.send(questionData);

}

// A function to get all questions
function get_questions(){

    // initialise the ajax request
    xhr = new XMLHttpRequest();

    // open request to get all questions
    xhr.open('GET', 'http://127.0.0.1:5000/questions/answers_count/');

    // Response from the server
    xhr.onload = function (onloadevent) {
        // sucessfully got all questions
        if (xhr.status == 200){

            // Changes the questions response text to a javascript array object
            const questions = JSON.parse(xhr.responseText);

            // display all questions

            // display variable
            let display_questions = '';

            // renders each question
            questions.questions.forEach(function render_question(element) {

                display_questions += `
                <div class="posted-question">
                    <!-- Upper section -->
                    <div class="upper-section">
                        <!-- user's name -->
                        <div class="name">
                            <a href="{{ url_for('signin.profile') }}" class="user-name">${element.whoposted}</a>
                            <p>${element.timeposted}</p>
                        </div>
                        <!-- Action options -->
                        <div class="options">
                            <!-- Three dots -->
                            <div class="three-dots">&#8942;</div>
                            <!-- Action options -->
                            <ul class="ul-options">
                                <li class="edit-question">&#x270E; Edit</li>
                                <li class="delete-question">&#10060; Delete</li>
                            </ul>
                        </div>
                    </div>
                    <!-- Question posted body -->
                    <div class="question-body">
                        <!-- question title -->
                        <a href="${element.questionid}/${element.title.split(" ").join("-")}" class="question-title">${element.title}</a>
                        <!-- Question description -->
                        <p>${element.description}</p>
                        <p>${element.answers} answer</p>
                    </div>
                    <!-- Edit question div -->
                    <div class="edit-question-errors">
                        <li></li>
                    </div>
                    <div class="edit-div">
                        <form enctype="multipart/form-data" data-questionid=${element.questionid} class="edit-form">
                            <input type="text" name="title" class="edit-question-title" placeholder="Edit question title...">
                            <textarea class="edit-question-description" name="description" placeholder="Edit question description..." cols="30" rows="10"></textarea>
                            <div class="cancel-submit">
                                <input type="button" class="cancel-button" value="cancel">
                                <input type="submit" name="submit-edited-question" class="submit-edited-question" value="save">
                            </div>
                        </form>
                    </div>
                    <!-- Confirm delete -->
                    <div class="confirm-question-delete-background">
                        <!-- Confirm delete question dialog box -->
                        <div class="confirm-question-delete">
                            <div class="confirm-question-delete-title">
                                <h4>Delete question</h4>
                            </div>
                            <div class="confirm-question-delete-body">
                                <h5>Are you sure you want to delete the question ?</h5>
                            </div>
                            <div class="confirm-question-delete-footer">
                                <input type="button" class="delete-question-cancel" value="cancel">
                                <input type="button" onclick="delete_question(${element.questionid})" class="delete-question-delete" value="delete">
                            </div>
                        </div>
                    </div>
                    <!-- End of edit question div -->
                </div>
                `;
            });
            document.querySelector('#posted-questions').innerHTML = display_questions;

        }
    };

    // sends the request
    xhr.send();
}

document.body.addEventListener('submit', editQuestion);

// A function to edit a question
function editQuestion(e){
    if(e.target.classList.contains('edit-form')){

        e.preventDefault();

        // gets the question id
        let question_id = e.target.getAttribute("data-questionid");
        
        // Changes the question id string to an integer
        let int_question_id = parseInt(question_id);

        // Grabs form data to be sent to the server by an ajax request
        let editquestionform = e.target;
        let editedquestionData = new FormData(editquestionform);

        // initialises ajax request object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('PUT', `http://127.0.0.1:5000/questions/${int_question_id}`);

        // What should happen if the reponse received from the server
        xhr.onload = function(onloadevent){

            // successful posted question
            if (xhr.status == 200){

                // display all questions
                get_questions();

            }
            else{

                // Response error from the server
                let error = JSON.parse(xhr.responseText);

                // // Gets the error div container
                let errorDiv = e.target.parentNode.previousElementSibling;

                // // Accesses the list tag to display the error
                let listErrorTag = errorDiv.children[0];

                // // if the list tag doesn't contain an error message,
                // // add one.
                if(listErrorTag.innerHTML == ''){
                    listErrorTag.innerHTML = error.error;
                }
                else{
                    // If list tag has an error text replace it with a new one
                    listErrorTag.innerHTML = error.error;
                }

                // // Display the error container, to display the error,
                // // message.
                errorDiv.style.maxHeight = errorDiv.scrollHeight + 'px';

                // Deletes all list error tags after 30 seconds
                setTimeout(function(){

                    // Replace the current error text with an empty string
                    listErrorTag.innerHTML = '';

                    // Makes the error container to disappear
                    errorDiv.style.maxHeight = 0 + 'px';

                }, 3000);      
            }
        };

        // Sends the request with the edited question
        xhr.send(editedquestionData);
    }
}


// Deletes a question
function delete_question(question_id){
    
    // instantiates the xhr
    xhr = new XMLHttpRequest();

    // opens the request to delete the question
    xhr.open('DELETE', `http://127.0.0.1:5000/questions/${question_id}`);

    // the request was successfully sent to the server
    xhr.onload = function(onloadevent){
        
        // successfully deleted the question
        if (xhr.status == 200){
            
            get_questions();
            
        }
        else{

            // The question doesn't exist error
            const error = JSON.parse(xhr.responseText);

        }
    };

    // sends the request to delete the question
    xhr.send();

}

// Renders all questions when the page loads
get_questions();
