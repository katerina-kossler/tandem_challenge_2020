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

 
def is_game_end(all_questions, answered_questions):
    """Checks if either 10 questions have been answered or all (available) questions have been answered."""
    available_questions = len(all_questions.keys())
    used_questions = len(answered_questions)
    
    if (used_questions == 10) or (used_questions == available_questions):
        return True
    else:
        return False


def select_question(questions):
    
    
    return selected_question


def display_question_and_options(current_question,questions,question_options):
    """"""
    pass


def get_user_answer(options):
    """"""
    pass

def is_answer_correct():
    """"""
    pass


def reveal_correct_answer(answer, correct):
    """"""
    pass


def update_score(answer, correct_answer, score):
    pass


def display_score(score, answered_questions, final=False):
    if final:
        return "Your final score is {} out of {}!".format(score, len(answered_questions))
    else:
        return "Your Score is now {}".format()


def is_user_playing_again():
    pass


def play_game():
    """Holds game logic and continues question asking and answering until the first of the following conditions is met:
        1) 10 questions are answered
        2) All available questions are answered
        3) The game is exited with CTRL+C or Delete

        At game end, the current score is provided.  If condition 1 or 2 were reached, the player is asked if they would like to play again.  If not, the game exits.
    """
    
    try:
        # Playing is used to allow the user to continue playing rounds of trivia
        playing = True
        
        while playing:
            # Game is initialized by validating the input file, building the 'question bank' and initializing the score and 
            # the answered questions.
            input_file = get_input_file()
            questions, question_options, question_answers = process_question_data(input_file)
            score = 0
            answered_questions = set()
            
            while not is_game_end(questions, answered_questions):
                # chose question
                # wait for user answer
                # validate user answer
                # compare answer to user answer
                # if correct update and display score
                # if incorrect, reveal answer
            
            display_score(score, answered_questions, True)
            
            # ask the user if they would like to play again
            playing = is_user_playing_again()
            
            
    except KeyboardInterrupt:
        display_score(score, answered_questions, True)
        

play_game()