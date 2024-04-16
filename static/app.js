class Chatbox{
    constructor(){
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
        }

        this.state = false;
        this.messages = [];
        this.isChatEnded = false;
        this.isFeedback = false;
        this.botAccuracy = 0;
        this.accuracyUpdate = 0;

        this.greetingsSet = new Set([
            "Hey :-)",
            "Hello, thanks for visiting",
            "Hi there, what can I do for you?",
            "Hi there, how can I help?",
            "See you later, thanks for visiting",
            "Have a nice day",
            "Bye! Come back again soon."
        ]);
        this.ratingAvailable = new Set([
            '1', '2', '3', '4', '5'
        ]);
    }

    display(){
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => {this.toogleState(chatBox)})
        sendButton.addEventListener('click', () => {this.onSendButton(chatBox)})
    
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) =>{
            if(key === "Enter"){
                this.onSendButton(chatBox)
            }
        })
    }

    toogleState(chatbox){
        this.state = !this.state;

        if(this.state){
            chatbox.classList.add('chatbox--active')
        }
        else{
            chatbox.classList.remove('chatbox--active')
        }
    }

    // isChatEnded = false;
    onSendButton(chatbox){
        var textField = chatbox.querySelector('input');
        let text1 = textField.value

        if(text1 === ""){
            return ;
        }

        let userText = text1;
        userText = userText.charAt(0).toUpperCase() + userText.slice(1);
        let msg1 = {name: "User", message: userText}
        
        this.messages.push(msg1);

        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type' : 'application/json'
            }
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = {name : "Sam", message: r.answer};
            let msg3 = {name : "Sam", message: 'Do you have any other questions?'};
            let feebackTest = {name : "Sam", 
            message: 'Time for feedback: 5.Excellent 4.Good 3.Average 2.Poor 1.Worst'};
            let botFeedback = {name : "Sam", message: 'You chose : ' + text1};
            
            
            console.log(this.isChatEnded);
            if(this.isChatEnded && text1.toLowerCase() == "no"){
                // Feedback hits
                this.isFeedback = true;
                this.messages.push(feebackTest);
                // this.showFeedbackOptions(chatbox);
            }
            else if(this.isChatEnded && text1.toLowerCase() == "yes"){    
                this.messages.push({name : "Sam", message: 'Feel free to ask!'});
                this.isChatEnded = false;
                this.isFeedback = false;
            }
            else if(r.answer != "I do not understand..."){
                this.messages.push(msg2);

                if (this.greetingsSet.has(r.answer)){
                    this.isChatEnded = false;
                    this.isFeedback = false;
                }
                else {
                    this.messages.push(msg3);
                    this.isChatEnded = true;
                }
                this.isFeedback = false;
            }
            else if(this.isFeedback){
                if(this.ratingAvailable.has(text1)){

                    if(text1 === '1'){
                        this.messages.push({name : "Sam", message: "Regrest! But don't worry our doubt assistant will contact you soon or call us on 1800-123-456 for escalation."});
                    }
                    else if(text1 === '2' || text1 === '3'){
                        this.messages.push({name : "Sam", message: "Provide us feedback to improve"});
                    }
                    
                    fetch('/update_metrics', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ Timestamp: new Date(),Rating: text1})
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });

                    this.messages.push(botFeedback);
                    this.messages.push({name : "Sam", message: 'Thank you for connecting with us!'});
                    var html = '';
                    const chatmessage = chatbox.querySelector('.chatbox__messages');
                    chatmessage.innerHTML = html;
                    this.isFeedback = false;
                }
                else{
                    this.messages.push({name : "Sam", message: 'Wrong choice! Try again'});
                }
            }
            else{
                this.isFeedback = false;
                this.isChatEnded = false;
                this.messages.push(msg2);
            } 
            
            console.log(this.isChatEnded);
            console.log(text1.toLowerCase());

            this.updateChatText(chatbox)
            textField.value = ''
        }).catch((error) =>{
            console.error(error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    // showFeedbackOptions(chatbox) {
    //     console.log("Showing feedback options...");
    //     let html = '<div class="messages__item messages__item--operator">' +
    //         '<p>Please provide your feedback:</p>' +
    //         '<div>' +
    //         '<input type="radio" id="satisfied" name="feedback" value="satisfied">' +
    //         '<label for="satisfied">Satisfied</label>' +
    //         '</div>' +
    //         '<div>' +
    //         '<input type="radio" id="neutral" name="feedback" value="neutral">' +
    //         '<label for="neutral">Neutral</label>' +
    //         '</div>' +
    //         '<div>' +
    //         '<input type="radio" id="unsatisfied" name="feedback" value="unsatisfied">' +
    //         '<label for="unsatisfied">Unsatisfied</label>' +
    //         '</div>' +
    //         '</div>';
    //     const chatmessage = chatbox.querySelector('.chatbox__messages');
    //     console.log("Chat message before: ", chatmessage);
    //     chatmessage.innerHTML += html;
    //     console.log("Chat message after:", chatmessage);
    //     // console.log("Feedback options added to chat message.");
    // }
    

    updateChatText(chatbox){
        var html = '';

        this.messages.slice().reverse().forEach(function(item, index){
            if(item.name === "Sam"){
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else{
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });
    
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();


















