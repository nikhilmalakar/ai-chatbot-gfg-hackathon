import random
import json
import torch
import csv
from datetime import datetime

from templates.doubtAssist.addQuestion import add_question

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

class ChatMessage:
    def __init__(self, timestamp, user, bot_response, accuracy, query):
        self.timestamp = timestamp
        self.user = user
        self.query = query
        self.bot_response = bot_response
        self.accuracy = accuracy
        
def save_to_csv(chat_message):
    with open('./database/chatDatabase.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'User', 'Query', 'Bot Response', 'Accuracy' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:  # If file is empty, write header
            writer.writeheader()

        writer.writerow({
            'Timestamp': chat_message.timestamp,
            'User': chat_message.user,
            'Query': chat_message.query,
            'Bot Response': chat_message.bot_response,
            'Accuracy': chat_message.accuracy
        })
        
        
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"



def get_response(msg, email):
    global unable_to_respond_count 
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    # print(prob.item())
    
    isFound = False
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                isFound = True
                response = random.choice(intent['responses'])
    
    if isFound == False:
        response = "I do not understand..."
         
#------- WRITE LOGIC TO DETECT UNRESOLVED NEW QUERIES ------------------------------------------------------
    # ADD QUERY RESPONSE TO DATABASE
    # TRAIN THE MODEL AGAIN
    # elif prob.item() > 0.5 :
    #     print("Send it to Dount Assistant")
    #     print(msg)
    add_question(msg)
    msg = msg.replace('"', '').replace("'", "")
    response = response.replace('"', '').replace("'", "")

    timestamp = datetime.now()
    chat_message = ChatMessage(timestamp=timestamp, user=email, query=msg, bot_response=response, accuracy=prob.item())
    save_to_csv(chat_message)
    
    # if prob.item() > 0.75:
    #     another_question = input("Do you have another question? (yes/no): ")
    #     if another_question.lower() == "yes":
    #         return response  # Continue the conversation
    #     else:
    #         return "Thank you for chatting with me. Would you like to provide feedback?"
    if response == "I do not understand...":
            unable_to_respond_count += 1
    else:
        unable_to_respond_count = 0
    if(unable_to_respond_count > 2) :
        response = 'Cannot resolve! Our doubt assistant will contact you soon'
        unable_to_respond_count = 0
        
    return response


if __name__ == "__main__":
    
#----------- PERFORMANCE METRICS ------------------------------------------------------
        # Response time, accuracy of responses, user satisfaction ratings, etc.

    
    print("Let's chat! (type 'quit' to exit)")
    count = 0
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            
            
#----------- WRITE LOGIC FEEDBACK MECHANISM ------------------------------------------------------
            # TAKE RATINGS
            # IF 4+ - EXIT
            # IF 2+ - ASK SUGGESTION
            # ELSE - further assistance or escalation options.
            
            
            break
        resp = get_response(sentence)
        
        if resp == "I do not understand...":
            count += 1
        else:
            count = 0
        if(count > 2) :
            print("sending to doubt assistant .....")
            count = 0
            
        print(resp)

