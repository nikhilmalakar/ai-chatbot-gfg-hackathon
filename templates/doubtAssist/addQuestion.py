from flask import Flask, render_template, request, jsonify, request, redirect,session
import csv
import os


def generate_question_id():
    try:
        os.path.exists('./templates/doubtAssist/questions.csv') and os.path.getsize('./templates/doubtAssist/questions.csv') > 0
        with open('./templates/doubtAssist/questions.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            questions = list(reader)
            last_question_id = int(questions[-1]['question_id'])
            new_question_id = last_question_id + 1
    except:
        new_question_id = 1
        
    return new_question_id

def add_question(question_text):
    question_id = generate_question_id()
    new_question = {
        'question_id': question_id,
        'question': question_text,
        'answer': ''
    }
    
    try:
        fieldnames = ['question_id', 'question', 'answer']
        with open('./templates/doubtAssist/questions.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if os.path.getsize('./templates/doubtAssist/questions.csv') == 0:
                writer.writeheader()
            writer.writerow(new_question)
            print(new_question)
            print("added successfully")
    
        
    except Exception as e:
        print("An error occurred:", e)

def load_questions_from_csv():
    questions = []
    with open('./templates/doubtAssist/questions.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions

def write_questions_to_csv(questions):
    fieldnames = ['question_id', 'question', 'answer']
    with open('./templates/doubtAssist/questions.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)


