# save this as app.py
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

#flask requiered app name
app = Flask(__name__)

#flask debugtoolbar settings
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 

# PAM: You have the avility to chose between two surveys. surveys = {"satisfaction": satisfaction_survey,"personality": personality_quiz}
selected_survey = surveys["satisfaction"] #focusing on this one for now
# selected_survey = surveys["personality"]

@app.route('/') #decorator expecting a function
def homepage(): #the function that will be executed when decorator is flagged
    """TODO: Step 2 Show homepage. 
    render template for startpage that shows the user the title of the survey, the instructions, and a button to start the survey.

    PAM: DONE

    TODO: Step 8: Storing answers in a list on the server.
    Use the session to store response information.

    To begin, modify your start page so that clicking on the button fires off a POST request to a new route that will set session[“responses”] to an empty list. The view function should then redirect you to the start of the survey. (This will also take care of the issue mentioned at the end of Step Six.) Then, modify your code so that you reference the session when you're trying to edit the list of responses.

    """
    
    return render_template("startpage.html", selected_survey=selected_survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """
    route from the pressing of the start button in the startpage, initializes responses of user and redirects user to first question of survey.
    """

    # initialize flask sesion saved cookie for user responses
    session["responses"] = []

    # redirect to first question
    return redirect('/questions/0')



@app.route('/questions/<int:question_id>')
def show_desired_question(question_id):
    """
    Renders the current question onto the webpage

    TODO: Step 3 PAM: DONE
    renders questions template for any question from the selected survey.
    Shows a form with the current question, listing choices as radio options, and a text field if a text field is allowed.
    Form's action is a post request to route /answer with the users answer.
   

    TODO: Step 6: Protecting Questions PAM: DONE
    condidtions for preventing users from falling out of line of the surveys progress 
    
    TODO: Step 7: Flash Messages
    Using flash, if the user does try to tinker with the URL and visit questions out of order, flash a message telling them they're trying to access an invalid question as part of your redirect.

    """
    RESPONSES = session["responses"] #STEP 8 Refactoring for flask session inclusion

    # Once they've answered all of the questions, trying to access any of the question pages should redirect them to the thank you page.

    if len(RESPONSES) == len(selected_survey.questions):

        flash(f"You have completed the survey. You can close this page now. You will never be able to restart the survey onece finished, as stated beforehand there is no going back.")
        
        return redirect("/Thank_you")

    # if user tries to go to a question id that doesn't exist, like /questions/7 , PAM: /question/-1? already handled by server, the dash from - turns that -1 into a string which is not the expected integer as we want...
    #  if the user has answered one survey question, but then tries to manually enter /questions/4 in the URL bar, you should redirect them to /questions/1.
    elif question_id > len(RESPONSES) or question_id < len(RESPONSES) or question_id > len(selected_survey.questions):

        flash(f"Plase Refrain from trying to skip questions or going to questions by manipulating the url.")
        
        question = selected_survey.questions[len(RESPONSES)]
        return render_template('question.html', question=question, question_id = len(RESPONSES),selected_survey=selected_survey)
    
    else:
        question = selected_survey.questions[question_id]

        return render_template('question.html', question=question, question_id = question_id,selected_survey=selected_survey)
        


@app.route('/answer', methods =["POST", "GET"])
def handle_question_answer():
    """
    Redirects user to next questions, saves previous answer to our Responses DB.

    TODO: Step 4 PAM: DONE so far
    Appends users answer to our fake DB object RESPONSES
    then send the user through a redirect to the next question.
    
    """
    # get the answer from the form data, if text answer was given add it as a tuple to answer element thatll be added to responses with their answer choice.
    # print(request.args["answer"])

    answer = request.args.get("answer")
    
    RESPONSES = session["responses"] #STEP 8 Refactoring for flask session inclusion
    # append answer to the fake DB
    RESPONSES.append(answer)
    session["responses"] = RESPONSES
    
    # move to the next question, assuming the user desnt stop and resubmit their question somehow X.X
    next_question_index = len(RESPONSES)
    """ 
    TODO: Step 5: 
    When survey is complete there wont be a next question so index will be out of range. directing user to a end of survey page.

    PAM: doing ... done i think...
    """
    if next_question_index < len(selected_survey.questions):
        return redirect(f"/questions/{next_question_index}")
    else:
        return redirect("/Thank_you")

@app.route('/Thank_you')
def redirect_to_thank_you_page():
    """render the thank you page"""

    RESPONSES = session["responses"] #STEP 8 Refactoring for flask session inclusion
    return render_template("thank_you.html", responses=RESPONSES)