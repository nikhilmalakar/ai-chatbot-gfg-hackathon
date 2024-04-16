***GFG Chatbot SDE Intern Hackathon***

GFG Chatbot is an AI-powered conversational assistant designed to provide helpful responses to user queries about a specific course or topic. It utilizes natural language processing techniques and a neural network model to understand user input and generate appropriate responses.

***Features***

Intent Recognition: The chatbot recognizes the intent behind user queries, allowing it to provide contextually relevant responses.
Dynamic Response Generation: Responses are generated dynamically based on the input query and the information available in the training data.
Feedback Mechanism: Includes a feedback mechanism to handle unresolved queries or user dissatisfaction, ensuring continuous improvement over time.
User Interaction: Engages users in meaningful conversations and offers assistance tailored to their needs.
Role-Based Login: Supports role-based login for normal users, doubt assistants, and administrators.
User Queries: Normal users can submit queries and receive meaningful answers from the chatbot.
Unresolved Query Handling: If a query remains unresolved, it is forwarded to the doubt assistant, who responds to it and adds it back to the database for future use.
Fallback to Doubt Assistant: If a user is not satisfied with the query results, the chatbot falls back to the doubt assistant for assistance.
Admin Dashboard: Administrators have access to an admin dashboard where they can:
Download All User Chats: Admins can download all user chats for training and analysis purposes.
View Performance Metrics: Track performance metrics such as feedback, accuracy, and other relevant statistics.
Download User Data: Admins can download all user data for further analysis and reporting.

***Installation***

Clone the repository to your local machine:

git clone https://github.com/nikhilmalakar/ai-chatbot-gfg-hackathon
Navigate to the project directory:

cd CourseChatbot
Set up a virtual environment using Anaconda:

conda create --name chatbot-env python=3.8
conda activate chatbot-env
Install the required dependencies:

pip install -r requirements.txt

***Usage***

Training the Chatbot:

Ensure you have your training data in the appropriate format (e.g., intents.json).
Run the train.py script to train the chatbot model using your data.

***Running the Chatbot:***

After training, you can interact with the chatbot using the Chat.py script.
Simply run the script and start typing your questions or queries.

***Login Details***

User - testuser@gmail.com 1234
Doubt Assitant - testassistant@gmail.com 1234
Admin - testadmin@gmail.com 1234
