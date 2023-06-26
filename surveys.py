class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=["Yes", "No"], allow_text=False):
        """Create question (assume Yes/No for choices.)
        PAM: Initializes a Question object.
        
        Args:
            question (str): The question text.
            choices (list, optional): The list of choices for the question. Defaults to ["Yes", "No"].
            allow_text (bool, optional): Defaults to False. Indicates whether text comments are allowed for the question. 
        
        """

        # PAM:Icommented this code block out because its better to just default choices to yes or no in the constructor definition
        # if not choices:
        #     choices = ["Yes", "No"] 

        self.choices = choices
        self.question = question
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire.
        PAM: Initializes a Survey object with a list of questions.
        
        Args:
            title (str): The name of the survey
            instructions (str): The neccesary information for how the user should complete the survey
            questions (list): The list of question instances
        """

        self.title = title
        self.instructions = instructions
        self.questions = questions

# PAM: Default data objects well use for our flask app.py, 2 instances of Survey with 4 instances of Question each.
satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
}