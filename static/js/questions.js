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
        let editQuestionTitle =  e.target.parentNode.parentNode.parentNode.parentNode.children[2].children[0].innerHTML;
        let editQuestionDescription =  e.target.parentNode.parentNode.parentNode.parentNode.children[2].children[1].innerHTML;

        // Hides the options window after the edit event.
        e.target.parentNode.style.display = "none";

        // Hides the posted question.
        e.target.parentNode.parentNode.parentNode.parentNode.children[2].style.maxHeight = 0 + "px";

        // Gets the form that would facilitate the editing of the question.
        let editQuestionFormElement = e.target.parentNode.parentNode.parentNode.parentNode.children[4].children[0];

        // gets the edit tags parent element
        let tagEditParentElement = editQuestionFormElement.children[2];

        // Gets the already posted tags to be displayed on the edit input text box.
        let tagParentElement = editQuestionFormElement.parentNode.previousElementSibling.previousElementSibling.children[2];
        let children = tagParentElement.children
        // Checks if the edit tag array has elements,
        // If so then it empty's the tag
        if(editTagsArray.length > 0){
            editTagsArray.splice(0,editTagsArray.length);
        }
        // Then adds the posted tags to the edit input text box automatically
        for(i=0; i<children.length; i++){
            // the trim method of the string to remove white spaces on both
            // sides of the text content
            editTagsArray.push(children[i].textContent.trim());
        }
        addEditTags(editTagsArray, tagEditParentElement);

        // Supplies the original posted text to the input and textarea elements of form for editing the question.
        editQuestionFormElement.children[0].value = editQuestionTitle;
        editQuestionFormElement.children[1].value = editQuestionDescription;
        
        // if the form is already open, closes it and places back the posted question.
        if(editQuestionFormElement.style.maxHeight == editQuestionFormElement.scrollHeight + "px"){
            editQuestionFormElement.style.maxHeight = 0 + "px";
            e.target.parentNode.parentNode.parentNode.parentNode.children[2].style.maxHeight = e.target.parentNode.parentNode.parentNode.parentNode.children[2].scrollHeight + "px";
        }
        else{
            // Else display the editing question form.
            editQuestionFormElement.style.maxHeight = editQuestionFormElement.scrollHeight + "px";
        }
    }
    else if(e.target.classList.contains('cancel-button')){
        // Closes the editing question form.
        e.target.parentNode.parentNode.parentNode.parentNode.children[4].children[0].style.maxHeight = null;
        e.target.parentNode.parentNode.parentNode.parentNode.children[2].style.maxHeight = e.target.parentNode.parentNode.parentNode.parentNode.children[2].scrollHeight + "px";
        // editTagsArray = [];
        editTagsArray.splice(0,editTagsArray.length);
        // console.log(editTagsArray);
        let tagParent = e.target.parentNode.previousElementSibling;
        resetEditTags(tagParent);
    }
    else if(e.target.id == 'question-image'){
        // Upload question image container clicked
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
    else if(e.target.classList.contains('edit-question-image-btn')){
        // Upload edited question image container clicked
        // uploads the edited image and displays its name on the button.
        let labelTag = e.target.nextElementSibling;
        e.target.addEventListener('change', function(event){
            // splits the string with a back slash and returns the last element
            // of the array which is the image's name.
            // This returns the last element of the array whicj is the name of the image.
            let imageName = event.target.value.split("\\").pop();
            if (imageName){
                // console.log(imageName);
                labelTag.innerHTML = imageName;
                // console.log(labelTag);
            }
            let editQuestionImageButton = e.target;
            // On change too display the edited question image to the user
            if (editQuestionImageButton.files && editQuestionImageButton.files[0]) {

                // An api to read contents of a image file content
                let editedQuestionImageReader = new FileReader();

                editedQuestionImageReader.onload = function(event) {

                // Gets image element to display the image
                    let displayImage = editQuestionImageButton.parentNode.parentNode.previousElementSibling.children[0];
                    // console.log(ditQuestionImageButtons.result);
                    // Changes image element source attribute
                    displayImage.src = event.target.result;
                    // console.log(event.target.result);

                    // Makes the parent container of the image big to fit the image
                    // console.log(displayImage.parentNode);
                    displayImage.parentNode.style.maxHeight =  displayImage.parentNode.scrollHeight + 'px';
                    // console.log(displayImage.parentNode);
                    editQuestionImageButton.parentNode.parentNode.previousElementSibling.parentNode.style.maxHeight =  displayImage.parentNode.parentNode.parentNode.parentNode.parentNode.scrollHeight + 'px';
                }
                    
                editedQuestionImageReader.readAsDataURL(e.target.files[0]); 
            }
        });
    }
    else if(e.target.id == 'logout-button'){
        sign_out_user();
    }
    else if(e.target.classList.contains('close-tag')){
        const tagData = e.target.getAttribute('data-tag');
        // Checks if the input text box is for editing the tag
        // removes the tag
        if(e.target.parentNode.parentNode.parentNode.classList.contains('edit-form')){
            const editIndex = editTagsArray.indexOf(tagData);
            // ... spread operator and slicing the array from start index to end index.
            editTagsArray = [...editTagsArray.slice(0, editIndex), ...editTagsArray.slice(editIndex  + 1)]
            addEditTags(editTagsArray, e.target.parentNode.parentNode);
        }
        // Remove the tag on creating the question
        else{
            const index = tagsArray.indexOf(tagData);
            // ... spread operator
            tagsArray = [...tagsArray.slice(0, index), ...tagsArray.slice(index + 1)]
            addTags();
        }
    }
    else if(e.target.id == 'bell-bell'){
        let notificationDropDown = e.target.parentNode.parentNode.children[2];
        shownotificationWindow(notificationDropDown);
        
    }
    else if(e.target.id == 'bell-div'){
        let notificationDropDown = e.target.parentNode.children[2];
        shownotificationWindow(notificationDropDown);
        
    }
    else if(e.target.id == 'bell'){
        let notificationDropDown = e.target.children[2];
        shownotificationWindow(notificationDropDown);
        
    }
    else if(e.target.id == 'badge'){
        let notificationDropDown = e.target.nextElementSibling;
        shownotificationWindow(notificationDropDown);
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
    // Adds the tag array value to the form data
    questionData.set('tags', JSON.stringify(tagsArray));
    // Emptys the the tags array, the first parameter specifies
    // the index to start to remove and the second parameter indicates how many
    //  elements to remove, in this case we are removing all elements so we take
    // the array length.
    tagsArray.splice(0,tagsArray.length);
    // After posting the question, remove all the tags from the input tag
    resetEditTags(questionform.children[2]);

    // initialise ajax request
    let xhr = new XMLHttpRequest();

    // open the request
    xhr.open('POST', `${base_url}/questions`, true);

    // What should happen if the reponse received from the server
    xhr.onload = function(onloadevent){

        // successful posted question
        if (xhr.status == 201){

            get_questions();

            // resets form data
            questionform.reset();

            // Displays successful message
            let questionMessageDiv = questionform.previousElementSibling;
            questionMessageDiv.innerHTML = "The question was successfully posted";
            questionMessageDiv.style.display = 'block';

            // Makes the flash message to disappear in 4 seconds
            setTimeout(function(){

                // Makes the message container to disappear
                questionMessageDiv.innerHTML = "";
                questionMessageDiv.style.display = 'none';

            }, 4000); 
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

            }, 3000);      
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
    xhr.open('GET', `${base_url}/questions/answers_count/`);

    // Response from the server
    xhr.onload = function (onloadevent) {
        // sucessfully got all questions
        if (xhr.status == 200){

            // Changes the questions response text to a javascript array object
            const questions = JSON.parse(xhr.responseText);
            console.log(questions);
            // display all questions

            // display variable
            let display_questions = '';

            // renders each question
            questions.questions.forEach(function render_question(element) {

                display_questions += `
                <div class="posted-question">
                    <div class="question-flash-messages">The question was edited</div>
                    <!-- Upper section -->
                    <div class="upper-section">
                        <!-- user's name -->
                        <div class="name">
                            <a href="${base_url}/profile" class="user-name">${element.whoposted}</a>
                            <p>${element.timeposted}</p>
                        </div>
                        <!-- Action options -->
                        <div class="options">
                            <!-- Three dots -->
                            ${element.is_author?'<div class="three-dots">&#8942;</div>':''}
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
                        <a href="${base_url}/questions/${element.questionid}/${element.title.split(" ").join("-")}" class="question-title">${element.title}</a>
                        <!-- Question description -->
                        <p>${element.description}</p>
                        <!-- Tags -->
                        <div class="tags">
                            ${ element.tags?
                                element.tags.map(tag =>`
                                <div>
                                  ${tag}
                                </div>              
                                `
                                ).join('')
                                :''
                            }
                        </div>
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
                            <!-- Edit tags -->
                            <div class="question-tags">
                                <input type="text" name="tags" class="tags-input" placeholder="Add a tag...">
                            </div>
                            <!-- Edited image container -->
                            <div class="edited-image">
                                <img class="the-edited-image" src="" alt="the edited image">
                            </div>
                            <div class="cancel-submit">
                                <div class="edit-question-image-container">
                                    <input type="file" name="edited-question-image" id=${"edit-question-image-btn"+element.questionid} class="edit-question-image-btn">
                                    <label for=${"edit-question-image-btn"+element.questionid}>
                                        <div class="edit-question-upload-image">
                                            <img src=${uploadImage} alt="edited question image" srcset="">
                                        </div>  
                                        Choose...
                                    </label>
                                </div>
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
                                <input type="button" onclick="delete_question(event, ${element.questionid})" class="delete-question-delete" value="delete">
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
        // Adds the tag array value to the form data
        editedquestionData.set('tags', JSON.stringify(editTagsArray));
        // Emptys the the tags array, the first parameter specifies
        // the index to start to remove and the second parameter indicates how many
        //  elements to remove, in this case we are removing all elements so we take
        // the array length.
        editTagsArray.splice(0,editTagsArray.length);
        // After posting the question, remove all the tags from the input tag
        resetEditTags(editquestionform.children[2]);

        // initialises ajax request object
        let xhr = new XMLHttpRequest();

        // opens the request
        xhr.open('PUT', `http://127.0.0.1:5000/questions/${int_question_id}`);

        // What should happen if the reponse received from the server
        xhr.onload = function(onloadevent){

            // successful posted question
            if (xhr.status == 200){

                const editedQuestion = JSON.parse(xhr.responseText);
            
                // Displays successful edition  message
                let questioneditedMessageDiv = e.target.parentNode.parentNode.children[0];
                // closes the editing form
                e.target.style.maxHeight = 0 + "px";
                // Gets all the tags
                tags_output = '';
                editedQuestion.editedquestion.tags.forEach(function(tag){
                    tags_output +=`
                    <div>
                    ${tag}
                     </div> 
                    `
                });

                // Displays the edited question
                // question title
                e.target.parentNode.parentNode.children[2].children[0].innerHTML = editedQuestion.editedquestion.title;
                // the description
                e.target.parentNode.parentNode.children[2].children[1].innerHTML = editedQuestion.editedquestion.description;
                // the tags
                e.target.parentNode.parentNode.children[2].children[2].innerHTML = tags_output;
                // Displays back the question container
                e.target.parentNode.parentNode.children[2].style.maxHeight = e.target.parentNode.parentNode.children[2].scrollHeight + "px";
                // Displays the flash message
                questioneditedMessageDiv.innerHTML = "The question was edited successfully";
                questioneditedMessageDiv.style.display = 'block';

                // Makes the flash message to disappear in 4 seconds
                setTimeout(function(){

                    // Makes the message container to disappear
                    questioneditedMessageDiv.innerHTML = "";
                    questioneditedMessageDiv.style.display = 'none';

                }, 4000); 

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
function delete_question(event, question_id){
    // closes the delete modal
    event.target.parentNode.parentNode.parentNode.style.display = "none";
    // Gets the flash message container
    let deleteMessageContainer = document.getElementById('question-added-flash-message');
    
    // instantiates the xhr
    xhr = new XMLHttpRequest();

    // opens the request to delete the question
    xhr.open('DELETE', `http://127.0.0.1:5000/questions/${question_id}`);

    // the request was successfully sent to the server
    xhr.onload = function(onloadevent){
        
        // successfully deleted the question
        if (xhr.status == 200){
            
            get_questions();
            // Displays the deletion successful massage
            deleteMessageContainer.innerHTML = "The question has been successfully deleted";
            deleteMessageContainer.style.backgroundColor = "rgba(255, 51, 0, 1)";
            deleteMessageContainer.style.display = "block";
            // Scroll to the top of page to see the error
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });
            // Makes the flash message to disappear in 4 seconds
            setTimeout(function(){

                // Makes the message container to disappear
                deleteMessageContainer.innerHTML = "";
                deleteMessageContainer.style.backgroundColor = "rgba(102, 153, 255, 1)";
                deleteMessageContainer.style.display = 'none';

            }, 4000); 
            
        }
        else{

            // The question doesn't exist error or unauthorized to delete it.
            const error = JSON.parse(xhr.responseText);
            // Displays the deletion denied error message
            deleteMessageContainer.innerHTML = error.error;
            deleteMessageContainer.style.backgroundColor = "rgba(255, 51, 0, 1)";
            deleteMessageContainer.style.display = "block";
            
            // Scroll to the top of page to see the error
            window.scroll({
                top: 0, 
                left: 0, 
                behavior: 'smooth' 
            });

            // Makes the flash message to disappear in 4 seconds
            setTimeout(function(){

                // Makes the message container to disappear
                deleteMessageContainer.innerHTML = "";
                deleteMessageContainer.style.backgroundColor = "rgba(102, 153, 255, 1)";
                deleteMessageContainer.style.display = 'none';

            }, 4000); 


        }
    };

    // sends the request to delete the question
    xhr.send();

}

// Gets user's name
function get_user_fullname(){

    // initialise ajax request object
    let xhr = new XMLHttpRequest();

    // opens the request
    xhr.open('POST', 'http://127.0.0.1:5000/questions/');

    // response from the server
    xhr.onload = function(onload){

        // sets the user name
        if(xhr.status == 200){

            user_name = JSON.parse(this.responseText);

            fullname_header = document.getElementById('user-fullname');

            fullname_header.innerHTML = user_name.fullname
        }
    }

    // sends the request
    xhr.send();
}

// Gets the base url
let base_url = window.location.origin;

let uploadImage = base_url + '/static/img/upload.png';
// console.log(uploadImage);


// Logs out a user
function sign_out_user(){
    
    // initialise ajax request object
    let xhr = new XMLHttpRequest();

    // opens the request
    xhr.open('GET', 'http://127.0.0.1:5000/logout');

    // response from the server
    xhr.onload = function(onload){

        // sets the user name
        if(xhr.status == 200){
            window.location.href = `${base_url}`
        }
    }

    // sends the request
    xhr.send();
}

// Runs the function to set the user name
get_user_fullname();

// Renders all questions when the page loads
get_questions();

// A method to display the notification dropdown
function shownotificationWindow(notificationWindow){
    if (notificationWindow.style.display == "grid"){
        notificationWindow.style.display = "none";
    }
    else{
        notificationWindow.style.display = 'grid';
    }
}



// ===================== Adding question's tags ======================
// A function to create a tag
function createQuestionTags(tagName){
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const labelSpan = document.createElement('span');
    labelSpan.setAttribute('class', 'label');
    labelSpan.innerHTML = tagName;
    const closeButton = document.createElement('span');
    closeButton.setAttribute('class', 'close-tag');
    closeButton.setAttribute('data-tag', tagName);
    closeButton.innerHTML = '&#9747;';
    div.appendChild(labelSpan);
    div.appendChild(closeButton);

    return div
}
// some data store for the tags
let tagsArray = [];

// Input text box container for the tags
questionTagContainer = document.querySelector('#question-tags');

// Input text box for the tags
tagsInput = document.querySelector('#tags-input');

// This is because the elements already exists on the interface, it will add
// identical tags, so they are all removed first.
function reset(){
    document.querySelectorAll('.tag').forEach(function(tag){
        tag.parentElement.removeChild(tag);
    });
}

// function to add the tags
function addTags(){
    
    reset();
    tagsArray.slice().reverse().forEach(function(tagvalue){
        const tagDiv = createQuestionTags(tagvalue);
        questionTagContainer.prepend(tagDiv);
    });
}

// A keyup event for adding a tag
tagsInput.addEventListener('keyup', function(e){
    if(e.key === 'Enter'){
        if (tagsInput.value === ''){
            console.log('Please provide a tag');
            let questionErrorContainer = tagsInput.parentNode.parentNode.parentNode.previousElementSibling;

            // Accesses the list tag to display the error
            let questionErrorTag = questionErrorContainer.children[0];
        
            // if the list tag doesn't contain an error message,
            // add one.
            if(questionErrorTag.innerHTML == ''){
                questionErrorTag.innerHTML = "Please provide a tag";
            }
            else{
                // If list tag has an error text replace it with a new one
                questionErrorTag.innerHTML = "Please provide a tag";
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
        
            }, 3000);
        
        }
        else{
            tagsArray.push(tagsInput.value);
            addTags();
            tagsInput.value = '';
        }
    }
});

// Prevent enter key from submiting a form but add a tag
// in the input textbox
document.body.addEventListener("keypress", function(e){
    if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
});



// ================== Adding tags on editing a question =====================
// Reset all tags with class 'tag' (removes all tags to be added a fresh)
function resetEditTags(parent){
    let children = parent.querySelectorAll('.tag');
    children.forEach(function(tag){
        parent.removeChild(tag);
    });
}

// A function to add tags in editing a question
function addEditTags(editTagsArray, container){
    resetEditTags(container);
    editTagsArray.slice().reverse().forEach(function(editTagvalue){
        const tagDiv = createQuestionTags(editTagvalue);
        container.prepend(tagDiv);
    });
}
// Listening to all key up events of the document
function keyUpActions(e){
    // Enter key up event
    if(e.key === 'Enter'){
        // some data store for the tags
        
        // Checks for the edit question input elements for tag 
        if(e.target.classList.contains('tags-input')){
            // grabs the input's element parent container
            let editTagParentContainer = e.target.parentNode;
            // grabs a tag value from the input
            let editTagvalue = e.target.value;
            // adds the value to the array
            editTagsArray.push(editTagvalue);
            if (e.target.offsetWidth < 50){
                console.log("You reached maximum number of tags")
            }
            // adds edit tags
            addEditTags(editTagsArray, editTagParentContainer);
            // clears the input value for the next tag
            e.target.value = '';
            let editQuestionFormElement = editTagParentContainer.parentNode;
            editQuestionFormElement.style.maxHeight = editQuestionFormElement.scrollHeight + "px";
        }
    }
}

// The listening of keyup events
document.body.addEventListener('keyup', keyUpActions);
let editTagsArray = [];



// ================== Display question image to be uploaded ==================
// Display question image to be uploaded
function readURL(input) {
    if (input.files && input.files[0]) {

      // An API to read contents of a image file content
      let questionImageReader = new FileReader();
      
      questionImageReader.onload = function(e) {
          // Gets image element to display the image
          let displayImage = document.getElementById("display-image");
          // Changes image element source attribute
          displayImage.src = e.target.result
          // Makes the parent container of the image big to fit the image
          displayImage.parentNode.style.maxHeight =  displayImage.parentNode.scrollHeight + 'px';
      }
      // Reads the image file uploaded 
      questionImageReader.readAsDataURL(input.files[0]); 
    }
}

// Gets the upload input image file element
let imageUploadInput = document.getElementById("question-image");

// triggers a change event on the upload button
// Listens to a change event
imageUploadInput.onchange = function(e){
    // reads the file and displays the image
    readURL(this);
}



// ================= Display edited question image to be uploaded ================
