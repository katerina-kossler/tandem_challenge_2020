import sys
import json
from exceptions import InputFileException, InputArgumentsException

# The following 3 keys are expected for each queston in the "json_questions" JSON-format, input file.
QUESTION_KEY = "question"
INCORRECT_OPTION_KEY = "incorrect"
ANSWER_KEY = "correct"
# Default question bank should be provided if not additional / custom questions are used.
DEFAULT_FILE = "Apprentice_TandemFor400_Data.json"


# The arguments passed in to the command line to run the game are validated to a one file input.
def get_input_file():
    """Validates that the question data is provided as the only other command line argument."""
    arguments = len(sys.argv)
    
    if arguments == 1:
        filename = DEFAULT_FILE
    elif arguments == 2:
        filename = sys.argv[1]
    else:
        raise InputArgumentsException
    
    return filename
    
    
# From the input file (json_questions), questions are parsed and validated into the "question_bank" of three 
# dictionaries for questions, question_options, and question_answers.
def get_key(key, question, question_id):
    """Validates the current key for the question and returns its value."""
    if question.get(key, None):
        return question[key]
    else:
        raise InputFileException(key, question_id)


def process_question_data(json_questions):
    """Takes in a JSON file of questions in the format:
    {"question": "<QUESTION>",
    "incorrect": ["<INCORRECT_OPTION_1>", ..., "<INCORRECT_OPTION_X>"],
    "correct": "<CORRECT_OPTION>"}
    
    Validates and processes the data into three dictionaries:
    1. questions: <QUESTION_ID>:<QUESTION_STRING>
        - a unifying question id makes it easy to connect the different pieces of information
    2. question_options: <QUESTION_ID>:set(["<OPTION_1>", ..., "<OPTION_X>"])
        - use a set to answers are unordered in printing out (introduces more randomness in option ordering)
    3. question_answers: <QUESTION_ID>:<ANSWER_STRING>
        - makes for relatively quick answer checking
    """

    questions = {}
    question_options = {}
    question_answers = {}
    
    if json_questions:
        with open(json_questions) as json_file:
            data = json.load(json_file)
            for current_question_id, current_question_map in enumerate(data):
                questions[current_question_id] = get_key(QUESTION_KEY, current_question_map, current_question_id)
                question_options[current_question_id] = set(get_key(INCORRECT_OPTION_KEY, current_question_map, current_question_id))
                question_answers[current_question_id] = get_key(ANSWER_KEY, current_question_map, current_question_id)
                question_options[current_question_id].add(question_answers[current_question_id])
                
    return (questions, question_options, question_answers) 

input_file = get_input_file()
questions, question_options, question_answers = process_question_data(input_file)
