// ====== Listens for click events on every element on the whole page =======\\
document.body.addEventListener('click', clickActions);

function clickActions(e){

    // edit element clicked
    if(e.target.classList.contains('edit-icon')){
        // Gets the answer tag
        let answerParagraph = e.target.parentNode.parentNode.nextElementSibling.children[0];
        // Gets edit div's container
        let editAnswerContainer = e.target.parentNode.parentNode.nextElementSibling.children[1];
        // Grabs the answer text value
        answerOriginalValue = answerParagraph.innerHTML;
        // Gets the textarea element and set the answer value
        // in it.
        textareaElement = editAnswerContainer.children[1].children[0];
        textareaElement.value = answerOriginalValue;
        textareaElement.style.maxHeight = textareaElement.scrollHeight + 'px';
        // Makes the answer paragraph tag disappear. setting
        // it's height 0
        answerParagraph.style.maxHeight = 0 + 'px';
        // Brings up the editor container and the editor
        editAnswerContainer.style.maxHeight =  editAnswerContainer.scrollHeight + 'px';
    }
    // closes edit container
    else if(e.target.classList.contains('cancel-button')){
        // gets the editor container
        editAnswerContainer = e.target.parentNode.parentNode.parentNode;
        // Closes the error container
        editAnswerContainer.children[0].style.maxHeight = 0 + 'px'
        // Gets the answer paragraph container
        answerParagraph = editAnswerContainer.previousElementSibling;
        // Closes the editor container
        editAnswerContainer.style.maxHeight = null;
        // Brings up the answer paragraph
        answerParagraph.style.maxHeight = answerParagraph.scrollHeight + 'px';
    }
    // displays delete modal
    else if(e.target.classList.contains('delete-icon')){
        let deleteModal = document.getElementById('delete-modal');
        deleteModal.style.display = "block";
    }
    // closes delete modal, background element
    else if(e.target.classList.contains('delete-modal')){
        e.target.style.display = 'none';
    }
    // closes delete modal, cancel button
    else if(e.target.classList.contains('delete-answer-cancel')){
        e.target.parentNode.parentNode.parentNode.style.display = 'none';
    }
    // deletes a question
    else if(e.target.classList.contains('delete-answer-delete-answerid')){
        let answerid = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute("data-del-answerid");
        // let editForm = e.target.parentNode.parentNode.parentNode.previousElementSibling.children[1];
        // let answerid = editForm.getAttribute("data-edit-answerid");
        // console.log(answerid);
        // Changes the answer id string to an integer
        let answer_id = parseInt(answerid);
        console.log(answer_id);
        delete_answer(e, answer_id, questionIdInt);
    }
    // Vote up or down arrows clicked
    else if(e.target.classList.contains('arrow-up') || e.target.classList.contains('arrow-down')){
        if (e.target.classList.contains('arrow-up')){
            // console.log("Vote up was clicked");
            let upvote_answerid = e.target.getAttribute("data-up-answerid");
            
            // Changes the answer id string to an integer
            let answerid = parseInt(upvote_answerid);
            // console.log(typeof answerid);
            voteForAnswer(e, 'upvote', answerid, questionIdInt);

        }
        else{
            // console.log("Vote down was clicked")
            let downvote_answerid = e.target.getAttribute("data-down-answerid");

            // Changes the answer id string to an integer
            let answerid = parseInt(downvote_answerid);
            // console.log(typeof answerid);
            voteForAnswer(e, 'downvote', answerid, questionIdInt);
            
        }
    }
    else{
        
    }

}


//====== Creates an answers line seperator =======\\
// selecting answers' container
let answers = document.querySelectorAll('#container #body-container #answers-container .user-answer');

if (answers){
    for(let i=0; i<answers.length; i++){
    // Creatting answers separator
    let createDivAnswerSeparator = document.createElement("div");
    // Adding class to the new div element
    createDivAnswerSeparator.className = 'answers-separator';
    answers[i].insertAdjacentElement("afterend", createDivAnswerSeparator);
    }
}

//====== A class that has all submit functions =======\\
class SubmitFunctions{

    static submitEditedAnswer(e, question_id){

        // gets the answer id
        let answer_id = e.target.getAttribute('data-edit-answerid');

        // Grabs form data to be sent to the server by an ajax request
        let editanswerform = e.target;
        let editedanswerData = new FormData(editanswerform);

        // initialises ajax request object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('PUT', `http://127.0.0.1:5000/answers/${answer_id}`)

        // gets the response from the server
        xhr.onload = function(onloadevent){
            
            // successfully edited the answer response
            if(xhr.status == 200){
                console.log(answer_id);
                get_question(question_id);
            }
            else{
                // response text error from server changed to javascript object
                const error = JSON.parse(xhr.responseText);

                // gets error div element
                let editErrorContainer = e.target.previousElementSibling;

                // Accesses the list tag to display the error
                let editErrorTag = editErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(editErrorTag.innerHTML == ''){

                    editErrorTag.innerHTML = error.error;
                }
                else{

                    // If list tag has an error text replace it with a new one
                    editErrorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                editErrorContainer.style.maxHeight = editErrorContainer.scrollHeight + 'px';

                // makes the errors disappear in 30 seconds
                setTimeout(function(){

                    // Replace the current error text with an empty string
                    editErrorTag.innerHTML = '';

                    // Makes the error container to disappear
                    editErrorContainer.style.maxHeight = null;
                }, 3000);
            }
        };

        // sends the edited answer
        xhr.send(editedanswerData);
    }


    static submitAnswer(e){
        // gets error div element
        let submitAnswerErrorContainer = e.target.parentNode.previousElementSibling;
        // Accesses the list tag to display the error
        let editErrorTag = submitAnswerErrorContainer.children[0];
        // if the list tag doesn't contain an error message,
        // add one.
        if(editErrorTag.innerHTML == ''){
            editErrorTag.innerHTML = "Please provide correct username and password";
        }
        else{
            // If list tag has an error text replace it with a new one
            editErrorTag.innerHTML = "Please fill all values to login";
        }
        // Display the error container, to display the error,
        // message.
        submitAnswerErrorContainer.style.maxHeight = submitAnswerErrorContainer.scrollHeight + 'px';
        // makes the errors disappear in 30 seconds
        setTimeout(function(){
            // Replace the current error text with an empty string
            editErrorTag.innerHTML = '';
            // Makes the error container to disappear
            submitAnswerErrorContainer.style.maxHeight = null;
        }, 3000);
    }

}

//======= Performs the submit events =======\\
document.body.addEventListener('submit', submitActions);


function submitActions(e){
    if(e.target.classList.contains('submit-edited-answer-form')){
        // Submits an edited answer

        // Prevent automatic route
        e.preventDefault();
        SubmitFunctions.submitEditedAnswer(e, questionIdInt);
    }
    else{
        
    }

}

// gets the URL search string, that is the path
let currentLocation = window.location.pathname;

// splits the url to an array and gets question's id as a string
let urlArray = currentLocation.split('/', 3);

// question's id as a string
let questionIdString = urlArray[2];

// Changes the question id string to an integer
let questionIdInt = parseInt(urlArray[2]);


// A function that gets the question and all it's answers
function get_question(questionId){

    // initialises the ajax request object
    xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('GET', `http://127.0.0.1:5000/questions/${questionId}`);

    // When the request has been processed
    xhr.onload = function (onloadevent){

        // the request was successful and the question was retrieved
        if(xhr.status == 200){

            // changes the response text to JavaScript Object
            let question = JSON.parse(xhr.responseText);

            // variable to display question title and description
            let title_description_html = '';

            // gets the question object
            let questionObject = question.Question;
            title_description_html +=`
                <div id="timeposted-section">posted: ${questionObject.timeposted}, views: 1 time</div>
                <!-- question title -->
                <div id="title-section">${questionObject.title}</div>
                <!-- question description -->
                <div id="description-section">${questionObject.description}</div>
                <div id="who-posted-image">
                    <img class="posted-by-image" src="http://127.0.0.1:5000/static/img/man.jpg" alt="posted by"> <a href="#">${questionObject.whoposted}</a>
                </div>
            `
            document.querySelector('#title-description-container').innerHTML = title_description_html;

            // answers variable to display all answers in html
            answers_html = '';

            // Checks if the answers array is not empty
            if(questionObject.answers && questionObject.answers.length){
                console.log(questionObject.answers);
                questionObject.answers.forEach(function(answer){
                answers_html += `
                <div class="user-answer" data-del-answerid=${answer.answerid}>
                    <!-- answer's number -->
                    <div class="answer-number">
                        <div class="arrow-up" data-up-answerid=${answer.answerid}></div>
                        <div class="votes">${answer.votes}</div>
                        <div class="arrow-down" data-down-answerid=${answer.answerid}></div>
                        <div class="vote-error-container">
                            You can not upvote an answer twice
                        </div>
                    </div>
                    <!-- answer header -->
                    <div class="answer-header">
                        <div class="edit-delete-icons">
                            <span class="edit-icon">&#x270E;</span>
                            <span class="delete-icon">&#10060;</span>
                        </div>
                        <div class="time-posted">${answer.time}</div>
                    </div>
                    <!-- answer div -->
                    <div class="the-answer">
                        <!-- answer on paragraph -->
                        <p>${answer.answer}</p>
                        <!-- end of paragraph answer -->
                        <!-- Form to edit an answer -->
                        <div class="edit-answer">
                            <!-- Editing answers errors -->
                            <div class="edit-answer-errors">
                                <li></li>
                            </div>
                            <form enctype="multipart/form-data" data-edit-answerid=${answer.answerid} class="submit-edited-answer-form">
                                <textarea name="answer" id="" cols="30" rows="15" placeholder="Edit answer..."></textarea>
                                <div class="cancel-submit">
                                    <input type="button" class="cancel-button" value="cancel">
                                    <input type="submit" name="submit-edited-answer" class="submit-edited-answer" value="save">
                                </div>
                            </form>
                        </div>
                        <!-- End of editing form -->
                        <!-- Confirm delete -->
                        <div class="confirm-delete-answer-background" id="delete-modal">
                            <!-- Confirm delete answer dialog box -->
                            <div class="confirm-delete-answer">
                                <div class="confirm-delete-answer-title">
                                    <h4>Delete answer</h4>
                                </div>
                                <div class="confirm-delete-answer-body">
                                    <h5>Are you sure you want to delete the answer ?</h5>
                                </div>
                                <div class="confirm-delete-answer-footer">
                                    <input type="button" class="delete-answer-cancel" value="cancel">
                                    <input type="button" class="delete-answer-delete delete-answer-delete-answerid" value="delete">
                                </div>
                            </div>
                        </div>
                        <!-- End of confirm delete -->
                    </div>
                    <!-- End of the answer div -->
                    <!-- answer's footer -->
                    <div class="answer-footer">
                        <div class="name-image">
                            <img src="http://127.0.0.1:5000/static/img/woman.jpg" alt="" srcset="">
                            <a href='http://127.0.0.1:5000/answers/${answer.answerid}'>${answer.whoanswered}</a>
                        </div>
                    </div>
                    <!-- End of votes -->
                </div>
                `
                let answers_container = document.querySelector("#answers-container");
                answers_container.innerHTML = answers_html;
                });
            }
            else{
                document.querySelector("#answers-container").innerHTML = `<p>No answers yet be the first to provide an answer</p>`;
                document.querySelector("#container #body-container #answer-errors").style.maxHeight= "0px";
            }

        }
        else{

            // Returns error if the question wasn't found
            let error = JSON.parse(xhr.responseText);  
        }
    };

    // Sends the request
    xhr.send();
}

// Runs the get question function
get_question(questionIdInt);

// Gets an answer's form id
submitAnswer = document.querySelector("#submit-answer-form");


function postAnswer(question_id){

    // A submit event to provide an answer to a question
    submitAnswer.addEventListener('submit', function(e){

        // Prvents action of the form from routing automatically
        e.preventDefault();

        // Grabs form data to be sent to the server by an ajax request
        let answerform = e.target;
        let answerData = new FormData(answerform);

        // creates a ajax request object
        xhr = new XMLHttpRequest();

        // opens the reques
        xhr.open('POST', `http://127.0.0.1:5000/answers/${question_id}`);

        // Response from the server
        xhr.onload = function (onloadevent) {

            // Answer submited successfully
            if (xhr.status == 201){

                // changes the response text to a javascript object 
                let answer = JSON.parse(xhr.responseText);
                get_question(question_id);

                // resets the form values
                answerform.reset();
            }
            else{
                // error response
                let error = JSON.parse(xhr.responseText);

                // gets error div element
                let submitAnswerErrorContainer = e.target.parentNode.previousElementSibling;

                // Accesses the list tag to display the error
                let editErrorTag = submitAnswerErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // add one.
                if(editErrorTag.innerHTML == ''){
                    editErrorTag.innerHTML = error.error;
                }
                else{

                    // If list tag has an error text replace it with a new one
                    editErrorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                submitAnswerErrorContainer.style.maxHeight = submitAnswerErrorContainer.scrollHeight + 'px';

                // makes the errors disappear in 30 seconds
                setTimeout(function(){

                    // Replace the current error text with an empty string
                    editErrorTag.innerHTML = '';

                    // Makes the error container to disappear
                    submitAnswerErrorContainer.style.maxHeight = null;
                }, 3000);
            }
        };

        // sends the answer
        xhr.send(answerData);


    });
}

// Calls a function to post answer
postAnswer(questionIdInt);

// A function to vote for an answer
function voteForAnswer(e, upordownvote, answerid, question_id){
    // initialise ajax request object
    let xhr = new XMLHttpRequest();

    // Opens the request
    xhr.open('POST', `http://127.0.0.1:5000/${upordownvote}/${answerid}/answer`);

    // Response from the server
    xhr.onload = function(onloadevent){
        // successful vote
        if (xhr.status == 201){
            get_question(question_id);
        }
        else{
            // Changes error response text to a javascript object
            let error = JSON.parse(this.responseText);

            // gets the error container
            let errorPopUpDiv = e.target.parentNode.children[3];
            
            // displays the error container
            errorPopUpDiv.style.display = 'flex';

            // places the error message to the container
            errorPopUpDiv.innerHTML = error.error;

            // makes the error disappear in 3 seconds
            setTimeout(function(){

                // clears the error message in the error container
                errorPopUpDiv.innerHTML = '';

                // hides the error container
                errorPopUpDiv.style.display = 'none';

            }, 3000);
        }
    };

    xhr.send()
}

// A function that deletes an answer
function delete_answer(e, answer_id, questionId){

    // initialises ajax request object
    let xhr = new XMLHttpRequest();

    // opens the request
    xhr.open('DELETE', `http://127.0.0.1:5000/answers/${answer_id}`);

    // response from the server
    xhr.onload = function(onloadevent){

        // answer successfully deleted
        if(xhr.status == 200){
            let delete_message = JSON.parse(xhr.responseText);
            get_question(questionId);
            // console.log(delete_message.message);
            let falsh_container = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[0];

            // displays the flash container
            falsh_container.style.display = 'flex';

            // Adds the message to the container
            falsh_container.innerHTML = delete_message.message;
            
            // makes the flash container to disappear in 4 seconds
            setTimeout(function() {

                // makes the container to disappear
                falsh_container.style.display = 'none';

                // makes sure it's content is empty after it disappears
                falsh_container.innerHTML = '';

            }, 4000);

        }
        else if(xhr.status === 403){
            // changes the response text to a javascript object
            let error = JSON.parse(xhr.responseText);
            get_question(questionId);
        
            let falsh_container = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[0];

            // displays the flash container
            falsh_container.style.display = 'flex';

            // changes the flash container background color to red
            falsh_container.style.backgroundColor = "red";

            // changes it's color opacity opacity


            // Adds the errorto the container
            falsh_container.innerHTML = error.error;
            
            // makes the flash container to disappear in 4 seconds
            setTimeout(function() {

                // makes the container to disappear
                falsh_container.style.display = 'none';

                // makes sure it's content is empty after it disappears
                falsh_container.innerHTML = '';

            }, 4000);

        }
        else{
            // error response
            let error= JSON.parse(xhr.responseText);
            console.log(error.error);
        }
    };

    // sends the delete request
    xhr.send();
}

let delete_buttons = document.getElementsByClassName('delete-answer-delete');
console.log(delete_buttons);

// Array.from(delete_buttons).forEach(function(button){
//     button.addEventListener('click', function(e){
//         console.log('clicked');
//     // console.log('data-wow value is: ' + element.dataset.wow);
//     let answerid = button.getAttribute("data-delete-answerid");
//     let answer_id = parseInt(answerid);
//     delete_answer(e, answer_id, questionIdInt);
//   });
// });


// Array.prototype.forEach.call(delete_buttons, function(button) {
//         button.addEventListener('click', function(e) {
//         // let answerid = button.getAttribute("data-delete-answerid");
//         let answerid = element.dataset.delete-answerid;
//         let answer_id = parseInt(answerid);
//         console.log('clicked');
//         delete_answer(e, answer_id, questionIdInt);

//     });
//   });