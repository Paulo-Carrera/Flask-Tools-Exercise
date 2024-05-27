from flask import Flask , request, redirect, render_template, flash, jsonify
from surveys import satisfaction_survey 

app = Flask(__name__)
app.config['SECRET_KEY']='P@ulo19'

responses = []      # List of user's responses


@app.route('/')
def home_page():
    """initial page to begin survey"""
    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route('/questions/<int:qid>')
def show_question(qid):             #Question ID argument
    """takes user through all questions in the survey with question ID"""
    if qid != len(responses):
        flash("Invalid question number.")
        return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question_num = qid , question = question)


@app.route('/answer' , methods=['POST'])
def handle_question():
    """handles collection of user responses and whether the survey is complete or not"""
    # Get the response choice
    choice = request.form['answer']

    # Append response to the responses list 
    responses.append(choice)

    if len(responses) == len(satisfaction_survey.questions):    # If all questions answered:
        return redirect('/complete')                            # Redirect to completion page
    else:
        return redirect(f'/questions/{len(responses)}')     # Else : redirect to next question


@app.route('/complete')
def complete():
    """when survey is complete, redirected to /complete and returns complete.html template"""
    return render_template('complete.html')  # When survey is complete , return 'complete.html' template


@app.route('/responses')    #   View list 'responses' 
def view_responses():
    """route to view users responses"""
    return jsonify(responses)


if __name__ == '__main__':
    app.run()

