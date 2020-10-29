import sys
import json

# json_question input file keys:
QUESTION_KEY = "question"
INCORRECT_OPTION_KEY = "incorrect"
ANSWER_KEY = "correct"

class InputFileException(Exception):
    """Exception raised for errors in the input file.
    
    Attributes: 
    - key
    - question_id
    """
    def __init__(self, key=None, question_id=0):
        self.key = key
        self.question_id = question_id
        self.message = "'{}' key is missing from question {}".format(key, question_id)
        super().__init__(self.message)


# process JSON file into a question bank through three dictionaries: questions, question_options, & question_answers
def get_key(key, question, question_id):
    """
    Validates the current key for the question and returns its value.
    """
    if question.get(key, None):
        return question[key]
    else:
        raise InputFileException(key, question_id)

# process JSON file into question bank
def process_question_data(json_questions):
    """
    Takes in a JSON file of questions in the format:
    
    "question": "<QUESTION>",
    "incorrect": ["<INCORRECT_OPTION_1>", ..., "<INCORRECT_OPTION_X>"],
    "correct": "<CORRECT_OPTION>"
    
    Processes the data into three dictionaries:
    
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
            # validate input file as objects are parsed
            data = json.load(json_file)
            for current_question_id, current_question_map in enumerate(data):
                # python_question = json.loads(json_question)
                print(current_question_id)
                questions[current_question_id] = get_key(QUESTION_KEY, current_question_map, current_question_id)
                question_options[current_question_id] = set(get_key(INCORRECT_OPTION_KEY, current_question_map, current_question_id))
                
                question_answers[current_question_id] = get_key(ANSWER_KEY, current_question_map, current_question_id)
                question_options[current_question_id] = question_options[current_question_id].add(question_answers[current_question_id])
                
    return (questions, question_options, question_answers) 

process_question_data(sys.argv[1])


# custom exceptions / more 

