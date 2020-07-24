// =========================Listens for click events on every element on the whole page===========\\
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
    else if(e.target.id == 'delete-modal'){
        e.target.style.display = 'none';
    }
    // closes delete modal, cancel button
    else if(e.target.id == 'delete-answer-cancel'){
        e.target.parentNode.parentNode.parentNode.style.display = 'none';
    }
    // Vote up or down arrows clicked
    else if(e.target.classList.contains('arrow-up') ||  e.target.classList.contains('arrow-down')){
        if (e.target.classList.contains('arrow-up')){
            console.log("Vote up was clicked");
        }
        else{
            console.log("Vote down was clicked")
        }
    }
    else{
        
    }

}



//======================================= Creates an answers line seperator ====================\\
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

//==========================A class that has all submit functions===============================\\
class SubmitFunctions{

    static submitEditedAnswer(e){
        // gets error div element
        let editErrorContainer = e.target.previousElementSibling;
        // Accesses the list tag to display the error
        let editErrorTag = editErrorContainer.children[0];
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
        editErrorContainer.style.maxHeight = editErrorContainer.scrollHeight + 'px';;
        // makes the errors disappear in 30 seconds
        setTimeout(function(){
            // Replace the current error text with an empty string
            editErrorTag.innerHTML = '';
            // Makes the error container to disappear
            editErrorContainer.style.maxHeight = null;
        }, 30000);
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

// ===================================== Performs the submit events =================================\\
document.body.addEventListener('submit', submitActions);


function submitActions(e){
    if(e.target.classList.contains('submit-edited-answer-form')){
        // Submits an edited answer

        // Prevent automatic route
        e.preventDefault();
        SubmitFunctions.submitEditedAnswer(e);
    }
    else if(e.target.classList.contains('submit-answer-input')){
        // Submits an answer

        // Prevent automatic route
        e.preventDefault();
        SubmitFunctions.submitAnswer(e);
    }
    else{
        console.log("Do nothing")
    }

}

// gets the URL search string, that is the path
let currentLocation = window.location.pathname;

// splits the url to an array and gets question's id as a string
let urlArray = currentLocation.split('/', 3);

// question's id as a string
let questionIdString = urlArray[2];

// Changes the id string to an integer
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
            console.log(question);

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
                    <img class="posted-by-image" src="{{ url_for('static', filename='img/man.jpg') }}" alt="posted by"> <a href="#">${questionObject.whoposted}</a>
                </div>
            `
            document.querySelector('#title-description-container').innerHTML = title_description_html;

            // answers variable to display all answers in html
            answers_html = '';

            // Checks if the answers array is not empty
            if(questionObject.answers){
                questionObject.answers.forEach(function(answer){

                answers_html += `
                <div class="user-answer">
                    <!-- answer's number -->
                    <div class="answer-number">
                        <div class="arrow-up"></div>
                        <div class="votes">${answer.votes}</div>
                        <div class="arrow-down"></div>
                    </div>
                    <!-- answer header -->
                    <div class="answer-header">
                        <div class="edit-delete-icons">
                            <span class="edit-icon">&#x270E;</span>
                            <span class="delete-icon">&#10060;</span>
                        </div>
                        <div class="time-posted">30 mins ago</div>
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
                            <form action="#" method="PUT" enctype="multipart/form-data" class="submit-edited-answer-form">
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
                            <div id="confirm-delete-answer">
                                <div id="confirm-delete-answer-title">
                                    <h4>Delete answer</h4>
                                </div>
                                <div id="confirm-delete-answer-body">
                                    <h5>Are you sure you want to delete the answer ?</h5>
                                </div>
                                <div id="confirm-delete-answer-footer">
                                    <input type="button" id="delete-answer-cancel" value="cancel">
                                    <input type="button" id="delete-answer-delete" value="delete">
                                </div>
                            </div>
                        </div>
                        <!-- End of confirm delete -->
                    </div>
                    <!-- End of the answer div -->
                    <!-- answer's footer -->
                    <div class="answer-footer">
                        <div class="name-image">
                            <img src="{{ url_for('static', filename='img/woman.jpg') }}" alt="" srcset="">
                            <a href="#">${answer.whoanswered}</a>
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
                answers_container.innerHTML = `<p>No answers yet be the first to provide an answer</p>`;
            }

        }
        else{
            // Returns error if the question wasn't found
            let error = JSON.parse(xhr.responseText);
            console.log(error);    
        }
    };
    // Sends the request
    xhr.send();
}

// Runs the get question function
get_question(questionIdInt);
