from flask import Flask, render_template,  send_file, url_for, request, jsonify, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import csv
from templates.doubtAssist.addQuestion import load_questions_from_csv, write_questions_to_csv
from chat import get_response

app = Flask(__name__)

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

bot_accuracy = 0
accuracy_updates = 0

# DATABASE SCHEMA FOR USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))

    def __init__(self,email,password,name, role):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


#---------------------- AUTH ROUTES --------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(name=name,email=email,password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['role'] = user.role
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    
    # FOR USER
    if session['email'] and session['role'] == "user":
        user = User.query.filter_by(email=session['email']).first()
        
        # fieldnames = ['email', 'name']
        is_present = False
        with open('./database/userDatabase.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == session['email']:
                    is_present = True
                    break
    
        if not is_present:
            with open('./database/userDatabase.csv', mode='a', newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow([session['email'], session['name']])
            
        return render_template('base.html', user=session)
    
    # FOR ADMIN
    elif session['email'] and session['role'] == "admin":
        user = User.query.filter_by(email=session['email']).first()
        return render_template('admin_dashboard.html',user=user)
    
    # FOR DOUBT ASSISTANT
    elif session['email'] and session['role'] == "assistant":
        user = User.query.filter_by(email=session['email']).first()
        
        questions = []
        with open('./templates/doubtAssist/questions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                questions.append(row)
            
        return render_template('assist_dashboard.html',user=user, questions=questions)
    
    return redirect('/login')

# START - ROUTES FOR DOUBT ASSISTANT  FUNCTIONALITY --------------------------------------------------------------
@app.route('/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    questions = load_questions_from_csv()
    updated_questions = [question for question in questions if int(question['question_id']) != question_id]
    write_questions_to_csv(updated_questions)
    return redirect(url_for('dashboard'))

@app.route('/answer/<int:question_id>', methods=['POST'])
def answer_question(question_id):
    answer = request.form['answer']
    questions = load_questions_from_csv()
    for question in questions:
        if int(question['question_id']) == question_id:
            question['answer'] = answer
    write_questions_to_csv(questions)
    return redirect(url_for('dashboard'))

# END - ROUTES FOR DOUBT ASSISTANT  FUNCTIONALITY --------------------------------------------------------------

@app.route('/download/chat-database')
def download_chat_data():
    file_path = './database/chatDatabase.csv'
    return send_file(file_path, as_attachment=True)

@app.route('/download/performance-metrics')
def download_performance_metrics():
    file_path = './database/feedbackDatabase.csv'
    return send_file(file_path, as_attachment=True)
@app.route('/download/user-database')
def download_user_data():
    file_path = './database/userDatabase.csv'
    return send_file(file_path, as_attachment=True)

@app.route('/update_metrics', methods=['POST'])
def update_csv():
    data = request.json
    with open('./database/feedbackDatabase.csv', 'a', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data['Timestamp'], session['email'], data['Rating'], bot_accuracy]) 


@app.route('/logout')
def logout():   
    session.pop('email',None)
    return redirect('/login')


#-----------------------------------------------------------------------------------
# @app.get("/")
# def index_get():
#     return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text, session['email'])
    message = {"answer" : response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True) 
    
    




