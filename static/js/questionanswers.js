// ====== Listens for click events on every element on the whole page =======\\
document.body.addEventListener('click', clickActions);

function clickActions(e){

    
    if(e.target.classList.contains('edit-icon')){
        // edit element clicked
        // Gets the answer tag
        let answerParagraph = e.target.parentNode.parentNode.nextElementSibling.children[1];
        // Hides the image container
            // answerParagraph.nextElementSibling.style.overflow = "hidden";
            // answerParagraph.nextElementSibling.style.maxHeight = 0 + 'px'
            answerParagraph.nextElementSibling.style.display = "none";
        // answerParagraph.nextElementSibling.children[0].style.maxHeight = 0 + 'px'
        // Gets edit div's container
        let editAnswerContainer = e.target.parentNode.parentNode.nextElementSibling.children[3];
        
        // Grabs the answer text value
        answerOriginalValue = answerParagraph.innerHTML;
        // Gets the textarea element and set the answer value
        // in it.
        textareaElement = editAnswerContainer.children[1].children[0];
        textareaElement.value = answerOriginalValue;
        textareaElement.style.maxHeight = textareaElement.scrollHeight + 'px';
        
        editAnswerContainer.children[1].style.maxHeight =  editAnswerContainer.children[1].scrollHeight + 'px';
        // editAnswerContainer.children[1].maxHeight = editAnswerContainer.children[1].scrollHeight + 'px';
        // Makes the answer paragraph tag disappear. setting
        // it's height 0
        answerParagraph.style.maxHeight = 0 + 'px';
        // Brings up the editor container and the editor
        // editAnswerContainer.children[0].style.maxHeight =  editAnswerContainer.children[0].scrollHeight + 'px';
        editAnswerContainer.children[1].style.maxHeight =  editAnswerContainer.children[1].scrollHeight + 'px';
        editAnswerContainer.style.maxHeight =  editAnswerContainer.scrollHeight + 'px';
    }
    else if(e.target.classList.contains('cancel-button')){
        // closes edit container
        // gets the editor container
        editAnswerContainer = e.target.parentNode.parentNode.parentNode;
        // Closes the error container
        editAnswerContainer.children[0].style.maxHeight = 0 + 'px';
        // editAnswerContainer.children[1].style.maxHeight = 0 + 'px';
        // gets the image container
        if(editAnswerContainer.previousElementSibling.children[0].getAttribute("src") != ""){
            editAnswerContainer.previousElementSibling.style.display = "block";
            window.scrollBy(0, -900);
        }
        else{
            // editAnswerContainer.previousElementSibling.maxHeight = 0 + "px";
            editAnswerContainer.previousElementSibling.style.display = "none";
        }
        // editAnswerContainer.previousElementSibling.style.maxHeight = editAnswerContainer.previousElementSibling.scrollHeight + 'px';
        // Gets the answer paragraph container
        let answerParagraph = editAnswerContainer.previousElementSibling.previousElementSibling;
        
        // Closes the editor container
        editAnswerContainer.style.maxHeight = 0 + 'px';
        // Brings up the answer paragraph
        answerParagraph.style.maxHeight = answerParagraph.scrollHeight + 'px';
        // Scrolls the window vertically up a bit
        // window.scrollBy(0, -200);
    }
    else if(e.target.classList.contains('edit-comment')){
        // Brings up the comment editing form
        let userContainer = e.target.parentNode;
        let commentContainer = e.target.parentNode.previousElementSibling;
        let comment = e.target.parentNode.previousElementSibling.innerHTML;
        let editcommentForm = e.target.parentNode.parentNode.children[3];
        editcommentForm.children[1].children[0].value = comment;
        userContainer.style.display = 'none';
        commentContainer.style.display = 'none';
        editcommentForm.style.display = 'grid';
    }
    else if(e.target.classList.contains('edit-comment-cancel')){
        // Closes editing comment container
        let form = e.target.parentNode.parentNode;
        let userContainer = form.previousElementSibling;
        let commentContainer = userContainer.previousElementSibling;
        userContainer.style.display = 'flex';
        commentContainer.style.display = 'block';
        form.style.display = 'none';
    }
    else if(e.target.classList.contains('delete-comment')){
        // Brings up confirm delete comment modal
        let deleteCommentModalContainer = e.target.parentNode.parentNode.children[4];
        deleteCommentModalContainer.style.display = 'block';
    }
    else if(e.target.classList.contains('confirm-delete-comment-background')){
        // Makes the confirm delete modal to disappear
        e.target.style.display = 'none';
    }
    else if(e.target.classList.contains('delete-comment-cancel')){
        // Closes the confirm delete comment modal when the cancel button is
        // clicked
        e.target.parentNode.parentNode.parentNode.style.display = 'none';

    }
    else if(e.target.classList.contains('delete-icon')){
        // displays delete modal
        let deleteModal = e.target.parentNode.parentNode.parentNode.children[2].children[4];
        deleteModal.style.display = "block";
    }
    else if(e.target.classList.contains('delete-modal')){
        // closes delete modal, background element
        e.target.style.display = 'none';
    }
    else if(e.target.classList.contains('delete-answer-cancel')){
        // closes delete modal, cancel button
        e.target.parentNode.parentNode.parentNode.style.display = 'none';
    }
    else if(e.target.classList.contains('arrow-up') || e.target.classList.contains('arrow-down')){
        // Vote up or down arrows clicked
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
    else if(e.target.classList.contains('answer-image-btn')){
        // Upload answer image buttonclicked
        // uploads the answer picture and displays its name on the button.
        let labelTag = e.target.nextElementSibling;
        e.target.addEventListener('change', function(event){
            // splits the string with a back slash and returns the last element
            // of the array which is the image's name.
            // This returns the last element of the array whicj is the name of the image.
            let imageName = event.target.value.split("\\").pop();
            if (imageName){
                labelTag.innerHTML = imageName;
            }
        });
    }
    else{
        
    }

}

function getImageName(uploadEvent){
    // Upload answer image buttonclicked
    // uploads the answer picture and displays its name on the button.
    let labelTag = uploadEvent.target.nextElementSibling;
    uploadEvent.target.addEventListener('change', function(event){
        // splits the string with a back slash and returns the last element
        // of the array which is the image's name.
        // This returns the last element of the array whicj is the name of the image.
        let imageName = event.target.value.split("\\").pop();
        if (imageName){
            labelTag.innerHTML = imageName;
        }
    });
}


//====== Creates an answers line seperator ====================
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



//====== A class that has all submit functions ================
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
        xhr.open('PUT', `${base_url}/answers/${answer_id}`)

        // gets the response from the server
        xhr.onload = function(onloadevent){
            
            // successfully edited the answer response
            if(xhr.status == 200){
                const answer_edited = JSON.parse(xhr.responseText);
                console.log(answer_edited);
                // get_question(question_id);
                // closes the editor's container
                e.target.parentNode.style.maxHeight = 0 + 'px';

                // Updates the new answer and displays it
                e.target.parentNode.parentNode.children[1].innerHTML = answer_edited.answeredited.answerEdited;
                e.target.parentNode.parentNode.children[1].style.maxHeight = e.target.parentNode.parentNode.children[1].scrollHeight + 'px';

                if(answer_edited.answeredited.editedimage != 'noimagekey'){
                    e.target.parentNode.previousElementSibling.children[0].src = base_url+"/static/img/"+answer_edited.answeredited.editedimage;
                    e.target.parentNode.previousElementSibling.style.display = "block";
                    window.scrollBy(0, -900);
                }
                else{
                    // editAnswerContainer.previousElementSibling.maxHeight = 0 + "px";
                    e.target.parentNode.previousElementSibling.style.display = "none";
                }
                // let falsh_container = document.getElementById("flash-messages");
                let falsh_container = e.target.parentNode.parentNode.children[0];
                // displays the flash container
                falsh_container.style.display = 'block';
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                // Adds the message to the container
                falsh_container.innerHTML = "The answer was successfully edited";
                
                // makes the flash container to disappear in 4 seconds
                setTimeout(function() {
    
                    // makes the container to disappear
                    falsh_container.style.display = 'none';
                    falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                    // makes sure it's content is empty after it disappears
                    falsh_container.innerHTML = '';
    
                }, 3000);
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

    static submitComment(e, answer_id){
        // Gets the form data
        let commentFormData = new FormData(e.target);

        // Initialize ajax request
        let xhr =new XMLHttpRequest();

        // open the request
        xhr.open('POST', `${base_url}/comments/${answer_id}/add_comment`);

        // Gets the response from the server
        xhr.onload = function(onloadevent){
            
            if(xhr.status == 201){
                // successfully added the comment

                // resets the comment form input text
                e.target.reset();
                get_question(questionIdInt);

                let falsh_container = document.getElementById("flash-messages");

                // displays the flash container
                falsh_container.style.display = 'block';
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                // Adds the message to the container
                falsh_container.innerHTML = "The comment was successfully added";
    
                // Scroll to the top of page to see the message
                window.scroll({
                    top: 0, 
                    left: 0, 
                    behavior: 'smooth' 
                });
                
                
                // makes the flash container to disappear in 4 seconds
                setTimeout(function() {
    
                    // makes the container to disappear
                    falsh_container.style.display = 'none';
                    falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                    // makes sure it's content is empty after it disappears
                    falsh_container.innerHTML = '';
    
                }, 4000);

            }
            else{
                // Posting a comment was unsuccessful
                const error = JSON.parse(xhr.responseText);
                console.log(error);
                // gets the error container
                let commetErrorContainer = e.target.parentNode.previousElementSibling;
                // gets the list (li) tag
                let errorTag = commetErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // adds one.
                if(errorTag.innerHTML == ''){

                    errorTag.innerHTML = error.error;
                }
                else{

                    // If list tag has an error text replace it with a new one
                    errorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                commetErrorContainer.style.maxHeight = commetErrorContainer.scrollHeight + 'px';

                // makes the errors disappear in 30 seconds
                setTimeout(function(){

                    // Replace the current error text with an empty string
                    errorTag.innerHTML = '';

                    // Makes the error container to disappear
                    commetErrorContainer.style.maxHeight = null;
                }, 3000);
            }
        }
        // Sends the request
        xhr.send(commentFormData);
    }

    static submitEditedComment(e, comment_id){
        // Gets the form data
        let commentEditFormData = new FormData(e.target);

        // Initialize ajax request
        let xhr =new XMLHttpRequest();

        // open the request
        xhr.open('PUT', `${base_url}/comments/${comment_id}/edit`);

        // Gets the response from the server
        xhr.onload = function(onloadevent){
            
            if(xhr.status == 200){
                // successfully edited the comment

                // resets the comment form input text
                e.target.reset();

                // get_question(questionIdInt);
                let comment = JSON.parse(xhr.responseText);
                console.log(comment);
                e.target.parentNode.children[1].innerHTML = comment.postedEditedComment.commentEdited;
                // Closes the editing form
                e.target.style.display = "none";
                // Displays the comment container new comment
                e.target.parentNode.children[1].style.display = "block";
                // Displays back the comment author's name
                e.target.parentNode.children[2].style.display = "flex";
                // Gets the comment flash message container
                let falsh_container = e.target.parentNode.children[0];

                // displays the flash container
                falsh_container.style.display = 'block';
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                // Adds the message to the container
                falsh_container.innerHTML = "The comment was successfully edited";
    
                
                // makes the flash container to disappear in 4 seconds
                setTimeout(function() {
    
                    // makes the container to disappear
                    falsh_container.style.display = 'none';
                    falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                    // makes sure it's content is empty after it disappears
                    falsh_container.innerHTML = '';
    
                }, 3000);

            }
            else{
                // Posting a comment was unsuccessful
                const error = JSON.parse(xhr.responseText);
                console.log(error);
                // gets the error container
                let commetErrorContainer = e.target.children[0];
                // gets the list (li) tag
                let errorTag = commetErrorContainer.children[0];

                // if the list tag doesn't contain an error message,
                // adds one.
                if(errorTag.innerHTML == ''){

                    errorTag.innerHTML = error.error;
                }
                else{

                    // If list tag has an error text replace it with a new one
                    errorTag.innerHTML = error.error;
                }

                // Display the error container, to display the error,
                // message.
                commetErrorContainer.style.maxHeight = commetErrorContainer.scrollHeight + 'px';

                // makes the errors disappear in 30 seconds
                setTimeout(function(){

                    // Replace the current error text with an empty string
                    errorTag.innerHTML = '';

                    // Makes the error container to disappear
                    commetErrorContainer.style.maxHeight = null;
                }, 3000);
            }
        }
        // Sends the request
        xhr.send(commentEditFormData);
    }

}




//======= Performs the submit events ===========================
document.body.addEventListener('submit', submitActions);
function submitActions(e){
    if(e.target.classList.contains('submit-edited-answer-form')){
        // Submits an edited answer

        // Prevent automatic route
        e.preventDefault();
        SubmitFunctions.submitEditedAnswer(e, questionIdInt);
    }
    else if(e.target.classList.contains("add-comment-form")){
        // Adding a comment
        // Prevent automatic route
        e.preventDefault();
        let answerToCommentTo = e.target.getAttribute("data-comment-answerid");
        SubmitFunctions.submitComment(e, answerToCommentTo);
        console.log(answerToCommentTo);
    }
    else if(e.target.classList.contains("edit-comment-form")){
        // Editting a comment
        // Prevent automatic route
        e.preventDefault();
        let commentToEdit = e.target.getAttribute("data-edit-comment");
        console.log('Comment edited '+commentToEdit);
        SubmitFunctions.submitEditedComment(e, commentToEdit);
        // console.log('Commented submited');
    }
    else{
        
    }

}



// gets the URL search string, that is the path
let currentLocation = window.location.pathname;

let base_url = window.location.origin;
console.log(base_url );


// splits the url to an array and gets question's id as a string
let urlArray = currentLocation.split('/', 3);


// question's id as a string
let questionIdString = urlArray[2];


// Changes the question id string to an integer
let questionIdInt = parseInt(urlArray[2]);


// ===========A function that gets the question and all it's answers=
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
            // http://127.0.0.1:5000/static/img/classes.jpg
            let questionObject = question.Question;
            document.querySelector('title').innerHTML = questionObject.title;
            title_description_html +=`
                <div id="timeposted-section">posted: ${questionObject.timeposted}, views: 2 times</div>
                <!-- question title -->
                <div id="title-section">${questionObject.title}</div>
                <!-- question description -->
                <div id="description-section">${questionObject.description}</div>
                <div id="posted-question-image-container">
                    <img src="${questionObject.image==="noimagekey"?"":base_url+"/static/img/"+questionObject.image}" alt="" class="posted-question-image" id="posted-question-image">
                </div>
                <div id="posted-image-modal">
                    <div>
                        <img src="" alt="" id="image-modal">
                    </div>
                </div>
                <div id="who-posted-image">
                    <img class="posted-by-image" src="${base_url}/static/img/man.jpg" alt="posted by"> <a href="#">${questionObject.whoposted}</a>
                </div>
            `
            document.querySelector('#title-description-container').innerHTML = title_description_html;

            // answers variable to display all answers in html
            answers_html = '';

            // Checks if the answers array is not empty
            if(questionObject.answers && questionObject.answers.length){
                
                questionObject.answers.forEach(function(answer){
                answers_html += `
                <div class="user-answer" data-del-answerid=${answer.answerid}>
                    <!-- answer's number -->
                    <div class="answer-number">
                        <div class="arrow-up" data-up-answerid=${answer.answerid}></div>
                        <div class="votes">${answer.votes}</div>
                        <div class="arrow-down" data-down-answerid=${answer.answerid}></div>
                        <div class="vote-error-container">
                        <!-- You can not upvote an answer twice -->
                        </div>
                        <div class="mark-answer-correct">
                            <span class="correct">&#10004</span> 
                        </div>
                    </div>
                    <!-- answer header -->
                    <div class="answer-header">
                        <div class="edit-delete-icons">
                            ${answer.is_author?'<span class="edit-icon">&#x270E;</span><span class="delete-icon">&#10060;</span>':''}
                        </div>
                        <div class="time-posted">${answer.time}</div>
                    </div>
                    <!-- answer div -->
                    <div class="the-answer">
                        <div class="answer-flash-message">The answer has been successfully edited</div>
                        <!-- answer on paragraph -->
                        <p>${answer.answer}</p>
                        <!-- end of paragraph answer -->
                        <div class="uploaded-answer-image">
                            <img class="the-uploaded-answer-image" src="${answer.answerimage==="noimagekey"?"":base_url+"/static/img/"+answer.answerimage}" alt="${answer.answerimage==="noimagekey"?"":"answer image"}">
                        </div>
                        <!-- Form to edit an answer -->
                        <div class="edit-answer">
                            <!-- Editing answers errors -->
                            <div class="edit-answer-errors">
                                <li></li>
                            </div>
                            <form enctype="multipart/form-data" data-edit-answerid=${answer.answerid} class="submit-edited-answer-form">
                                <textarea name="answer" id="" cols="30" rows="15" placeholder="Edit answer..."></textarea>
                                <!-- Display answer image container -->
                                <div class="edit-answer-image">
                                    <img id="the-edited-answer-image" class="the-edited-answer-image" src="" alt="the edited answer image">
                                </div>
                                <!-- cancel, submit and edit image button -->
                                <div class="cancel-submit">
                                    <div class="edit-answer-image-container">
                                        <input type="file" name="image" onclick="getImageName(event)" id="edit-answer-image-btn-${answer.answerid}" class="edit-answer-image-btn">
                                        <label for="edit-answer-image-btn-${answer.answerid}">
                                            <div class="edit-answer-upload-image">
                                                <img src="${base_url}/static/img/upload.png"  alt="image" srcset="">
                                            </div>  
                                            Choose...
                                        </label>
                                    </div>
                                    <input type="button" class="cancel-button" value="cancel">
                                    <input type="submit" name="submit-edited-answer" class="submit-edited-answer" value="save">
                                </div>
                            </form>
                        </div>
                        <!-- End of editing form -->
                        <!-- Confirm delete -->
                        <div class="confirm-delete-answer-background" class="delete-modal">
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
                                    <input type="button" onclick="delete_answer(event, ${answer.answerid}, ${questionIdInt})" class="delete-answer-delete" value="delete">
                                </div>
                            </div>
                        </div>
                        <!-- End of confirm delete -->
                    </div>
                    <!-- End of the answer div -->
                    <!-- answer's footer -->
                    <div class="answer-footer">
                        <div class="name-image">
                            <img src="${base_url}/static/img/woman.jpg" alt="" srcset="">
                            <a href='${base_url}/answers/${answer.answerid}'>${answer.whoanswered}</a>
                        </div>
                    </div>
                    <!-- Comments section-->
                    <div class="comments">
                        <!-- comment -->
                        <div class="coment-section">
                           ${answer.comments.length === 0?"":answer.comments.map(comment =>
                            `<div class="comment">
                                <div class="comment-flash-messages"></div>
                                <div class="the-comment" id="the-comment-${comment.commentid}">${comment.comment}</div>
                                <div class="user-comment">
                                    <a href="#">${comment.userwhocommented}</a>
                                    <img src="${base_url}/static/img/woman.jpg" alt="Andrew">
                                    ${comment.is_author?'<p class="edit-comment">Edit</p><p class="delete-comment">Delete</p> ':''}  
                                </div>
                                <form class="edit-comment-form" data-edit-comment=${comment.commentid}>
                                    <div class="comment-errors">
                                        <li></li>
                                    </div>
                                    <div class="edit-comment-div">
                                        <input type="text" class="edit-comment-input" name="comment">
                                    </div>
                                    <div class="edit-comment-submit-div">
                                        <input type="submit" class="edit-comment-submit" value="Save">
                                        <input type="button" class="edit-comment-cancel" value="Cancel">
                                    </div>
                                </form>
                                <div class="confirm-delete-comment-background" id="delete-comment-modal">
                                    <!-- Confirm delete comment dialog box -->
                                    <div class="confirm-delete-comment">
                                        <div class="confirm-delete-comment-title">
                                            <h4>Delete comment</h4>
                                        </div>
                                        <div class="confirm-delete-comment-body">
                                            <h5>Are you sure you want to delete the comment ?</h5>
                                        </div>
                                        <div class="confirm-delete-comment-footer">
                                            <input type="button" class="delete-comment-cancel" value="cancel">
                                            <input type="button" class="delete-comment-delete" value="delete" onclick="delete_comment(event, ${comment.commentid})" data-delete-comment=${comment.commentid}>
                                        </div>
                                    </div>
                                </div>
                                
                            </div>`
                            ).join('')}
                        </div>
                        <div class="add-comment-errors" >
                            <li>Please provide a comment</li>
                        </div>
                        <div class="add-comment">
                            <div class="add-comment-title">Add comment:</div>
                            <form class="add-comment-form" data-comment-answerid=${answer.answerid}>
                                <input type="text" name="comment" class="coment-text-box">
                                <input type="submit" name="submit-comment" class="submit-comment-button" value="Save">

                            </form>
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
            let notfounderror = JSON.parse(xhr.responseText);
            console.log(notfounderror);
        }
    };

    // Sends the request
    xhr.send();
}

// Runs the get question function
get_question(questionIdInt);


// Posts an answer
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

        // opens the request
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
                
                let falsh_container = document.getElementById("flash-messages");

                // displays the flash container
                falsh_container.style.display = 'block';
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
    
                // Adds the message to the container
                falsh_container.innerHTML = "The answer was successfully added";
    
                // Scroll to the top of page to see the message
                window.scroll({
                    top: 0, 
                    left: 0, 
                    behavior: 'smooth' 
                });
                           // makes the flash container to disappear in 4 seconds
                setTimeout(function() {

                    // makes the container to disappear
                    falsh_container.style.display = 'none';
                    falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";

                    // makes sure it's content is empty after it disappears
                    falsh_container.innerHTML = '';

                }, 4000);
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
            errorPopUpDiv.style.backgroundColor = "red";
            
            // displays the error container
            errorPopUpDiv.style.display = 'flex';

            // places the error message to the container
            errorPopUpDiv.innerHTML = error.error;

            // makes the error disappear in 3 seconds
            setTimeout(function(){

                // clears the error message in the error container
                errorPopUpDiv.innerHTML = '';
                errorPopUpDiv.style.backgroundColor = "red";
                // hides the error container
                errorPopUpDiv.style.display = 'none';

            }, 2000);
        }
    };

    xhr.send()
}



// A function that deletes an answer
function delete_answer(event, answer_id, questionId){

    // initialises ajax request object
    let xhr = new XMLHttpRequest();

    // opens the request
    xhr.open('DELETE', `http://127.0.0.1:5000/answers/${answer_id}`);

    // response from the server
    xhr.onload = function(onloadevent){

        // answer successfully deleted
        if(xhr.status == 200){
            let delete_message = JSON.parse(xhr.responseText);
            console.log(delete_message);
            get_question(questionId);
            // console.log(delete_message.message);
            let falsh_container = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[0];

            // displays the flash container
            falsh_container.style.display = 'block';

            // Adds the message to the container
            falsh_container.innerHTML = delete_message.message;
            falsh_container.style.backgroundColor = "red";

            // Scroll to the top of page to see the message
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });
            
            
            // makes the flash container to disappear in 4 seconds
            setTimeout(function() {

                // makes the container to disappear
                falsh_container.style.display = 'none';
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";

                // makes sure it's content is empty after it disappears
                falsh_container.innerHTML = '';

            }, 4000);

        }
        else if(xhr.status === 403){
            // changes the response text to a javascript object
            let error = JSON.parse(xhr.responseText);
            get_question(questionId);
        
            let falsh_container = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[0];

            // displays the flash container
            falsh_container.style.display = 'flex';

            // changes the flash container background color to red
            falsh_container.style.backgroundColor = "red";

            // changes it's color opacity opacity
            falsh_container.style.opacity = "0.7";

            // Adds the errorto the container
            falsh_container.innerHTML = error.error;

            // Scroll to the top of page to see the error
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });
            
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


// A function that deletes an answer
function delete_comment(event, comment_id){

    // initialises ajax request object
    let xhr = new XMLHttpRequest();

    // opens the request
    xhr.open('DELETE', `${base_url}/comments/${comment_id}/delete`);

    // response from the server
    xhr.onload = function(onloadevent){

        // answer successfully deleted
        if(xhr.status == 200){
            let delete_message = JSON.parse(xhr.responseText);
            console.log(delete_message);
            get_question(questionIdInt);
            // console.log(delete_message.message);
            let falsh_container = document.getElementById("flash-messages");
            // let falsh_container = e.target.parentNode.parentNode.parentNode.parentNode.children[0]

            // Displays the deletion successful massage
            falsh_container.innerHTML = delete_message.message;
            falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
            falsh_container.style.display = "block";
            // Scroll to the top of page to see the error
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });
            // Makes the flash message to disappear in 4 seconds
            setTimeout(function(){

                // Makes the message container to disappear
                falsh_container.innerHTML = "";
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
                falsh_container.style.display = 'none';

            }, 4000); 

        }
        else{
            // changes the response text to a javascript object
            let error = JSON.parse(xhr.responseText);
            // get_question(questionIdInt);

            let falsh_container = e.target.parentNode.parentNode.parentNode.parentNode.children[0]
            // let falsh_container = document.getElementById("flash-messages");

            // Displays the deletion successful massage
            falsh_container.innerHTML = error.error;
            falsh_container.style.backgroundColor = "rgba(255, 51, 0, 1)";
            falsh_container.style.display = "block";
            // Scroll to the top of page to see the error
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });
            // Makes the flash message to disappear in 4 seconds
            setTimeout(function(){

                // Makes the message container to disappear
                falsh_container.innerHTML = "";
                falsh_container.style.backgroundColor = "rgba(102, 153, 255, 1)";
                falsh_container.style.display = 'none';

            }, 4000); 

        }
    };

    // sends the delete request
    xhr.send();
}

// ================== Displays an answer picture to be uploaded ======
// Display answer image to be uploaded
function readURL(input) {
    if (input.files && input.files[0]) {
      // An api to read contents of a image file content
      let questionImageReader = new FileReader();
      
      questionImageReader.onload = function(e) {
          // Gets image element to display the image in it
          let displayImage = document.getElementById("the-answer-image");
          // Changes image element source attribute
          displayImage.src = e.target.result
          // Makes the parent container of the image big to fit the image
          displayImage.parentNode.style.maxHeight =  displayImage.parentNode.scrollHeight + 'px';
      }
      
      questionImageReader.readAsDataURL(input.files[0]); 
    }
}

// Gets the upload input image file element
let imageUploadInput = document.getElementById("answer-image-btn");

// triggers a change event on the upload button
// Listens to a change event
imageUploadInput.onchange = function(e){
    // reads the file and displays the image
    readURL(this);
}


// =================== Marks an answer correct ======================
// let allTicks = document.querySelectorAll('.correct');

// if(allTicks.length < 2){
//     console.log(allTicks.length);
//     allTicks[0].addEventListener('click', function(e){
//         if(allTicks[0].classList.contains("activetick")){
//             allTicks[0].className = allTicks[0].className.replace("activetick", "");
//         }
//         else{
//             allTicks[0].className += " activetick";
//         }
//     });
// }
// else{
//     console.log(allTicks.length);
//     for(i=0; i<allTicks.length; i++){
//         allTicks[i].addEventListener('click', function(e){
//             currentActiveTick = document.querySelectorAll('.activetick');
//             currentActiveTick[0].className = currentActiveTick[0].className.replace("activetick", "");
//             this.className += " activetick";
//         });
//     }
// }


