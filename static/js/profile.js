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
        }
        else{
            displayContent.hideContents(questions, updateProfile);
            displayContent.displayContents(profileInformation);         
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