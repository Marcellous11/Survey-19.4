from multiprocessing.connection import answer_challenge
from flask import Flask
from flask import render_template,redirect, session, request
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'

all_answers = []

@app.route('/')
def home_page():
    survey_title = survey.title
    survey_instructions = survey.instructions
    return render_template('home.html',title=survey_title,instructions=survey_instructions)

@app.route('/answer')
def answer_handler():
    current_q = len(all_answers)
    choice = request.args['answer']
    session[f'{survey.questions[current_q].question}'] = choice
    all_answers.append(choice)
    return redirect(f'/questions/{current_q}')

@app.route('/questions/<int:qid>')
def questions(qid):
    current_q = len(all_answers)
    if(qid != current_q):
        return redirect(f'/questions/{current_q}')

    if(current_q == len(survey.questions)):
        return render_template('/completed.html')
    else:
        s_questions=survey.questions[qid]
        return render_template(f'questions.html',questions=s_questions)

    

    
