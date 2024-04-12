import random
import json
import torch

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from templates.doubtAssist.addQuestion import add_question

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

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
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
#------- WRITE LOGIC TO DETECT UNRESOLVED NEW QUERIES ------------------------------------------------------
    # ADD QUERY RESPONSE TO DATABASE
    # TRAIN THE MODEL AGAIN
    # elif prob.item() > 0.5 :
    #     print("Send it to Dount Assistant")
    #     print(msg)
    add_question(msg)
    return "I do not understand..."


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
            
#----------- ADD CHAT TRANSCRIPT OF USER TO DATABASE ------------------------------------------------------
            # USER ID WITH CHATS SCRIPT
            # IN CSV FORMAT
            
            break
        resp = get_response(sentence)
        
        if resp == "I do not understand...":
            count += 1
        else:
            count = 0
        if(count > 2) :
#----------- WRITE LOGIC TO SEND TO DOUBT ASSISTANT ------------------------------------------------------
            # CAN PROVIDE CONTACT DETAILS OF DOUBT ASSISTANT
            # OR HE CAN CONTACT USER
            # REDIRECT TO 1V1 RESOLUTION
            print("sending to doubt assistant .....")
            count = 0
            
        print(resp)

