from crypt import methods
from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "programming"

#for Flask debug tool turn redirect prompt to off
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#responses = []

@app.route('/')
def home_page():
    """returns the home page"""
    return render_template('home.html', survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():
    session["responses"] = []
    return redirect ('/questions/0')


@app.route('/answer', methods=['POST'])
def get_answer():
    
    response = request.form['radio']

    responses = session["responses"]
    responses.append(response)
    session["response"] = responses


    if len(responses) >= len(survey.questions):
        return redirect ('/completed')
    else:
        return redirect (f'/questions/{len(responses)}')


@app.route('/questions/<int:index>')
def show_question(index):
    responses = session["responses"]

    if responses == None:
        return redirect('/')

# if accessing questions out of order.
    if (len(responses) != index):
        flash(f"Accessing invalid question! FORBIDDEN!! ACHTUNG!! Continue with current question.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[index]

# if accessing out-of-bound question
    if len(responses) >= len(survey.questions):
        return redirect ('/completed')

    return render_template('questions.html', question=question)


@app.route('/completed')
def completed():
    r=session["responses"]
    return render_template('/completed.html', r=r)

