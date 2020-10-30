from os import name, system
from sys import argv, exit
from json import load
from exceptions import InputFileException, InputArgumentsException
from random import randrange

# The following 3 keys are expected for each queston in the "json_questions" JSON-format, input file.
QUESTION_KEY = "question"
INCORRECT_OPTION_KEY = "incorrect"
ANSWER_KEY = "correct"
# Default question bank should be provided if not additional / custom questions are used.
DEFAULT_FILE = "Apprentice_TandemFor400_Data.json"


def clear_terminal_window():
    """Clears the terminal for clarity based on the os name.  Windows uses a command of 'cls' while Max and Linux use 'clear'."""
    if name == 'nt': 
        system('cls') 
    else: 
        system('clear')


# The arguments passed in to the command line to run the game are validated to a one file input.
def get_input_file():
    """Validates that the question data is provided as the only other command line argument."""
    arguments = len(argv)
    if arguments == 1:
        filename = DEFAULT_FILE
    elif arguments == 2:
        filename = argv[1]
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
            data = load(json_file)
            for current_question_id, current_question_map in enumerate(data, 1):
                questions[current_question_id] = get_key(QUESTION_KEY, current_question_map, current_question_id)
                question_options[current_question_id] = set(get_key(INCORRECT_OPTION_KEY, current_question_map, current_question_id))
                question_answers[current_question_id] = get_key(ANSWER_KEY, current_question_map, current_question_id)
                question_options[current_question_id].add(question_answers[current_question_id])
    return (questions, question_options, question_answers) 



def pause_for_user():
    """Waits for user to hit enter to continue so they have time to review the current screen."""
    input("Hit enter when you are ready to continue.")
     
 
def explain_game():
    """Outputs the basic gameplay for this trivia game"""
    print("""
    Welcome to the hottest new CLI game to hit your terminal!
     ______               __               ___              ____  ___   ___   __
    /_  __/___ _ ___  ___/ /___  __ _     / _/___   ____   / / / / _ \ / _ \ / /
     / /  / _ `// _ \/ _  // -_)/  ' \   / _// _ \ / __/  /_  _// // // // //_/ 
    /_/   \_,_//_//_/\_,_/ \__//_/_/_/  /_/  \___//_/      /_/  \___/ \___/(_)  
                                                                                
    """)
    print("""
    Using the JSON file you passed in as an argument (or the default file 
    if you didn't provide one), we will build a randomized round of trivia
    for you to answer!
    
    Each round of trivia will consist of 10 questions (if possible).
    For each question, type in your selection and hit enter.
        
    Leave at any point using Ctrl+C. 
    """)
    pause_for_user()
 
 
def is_game_end(all_questions, answered_questions):
    """Checks if either 10 questions have been answered or all (available) questions have been answered."""
    available_questions = len(all_questions.keys())
    used_questions = len(answered_questions)
    if (used_questions == 10) or (used_questions == available_questions):
        return True
    else:
        return False


def select_question(questions, answered_questions):
    """Selects a new question at random from a set of question numbers until an unasked question is chosen"""
    limit = len(questions)
    seen = True
    while seen:
        selected_question = randrange(0, limit)
        if not selected_question in answered_questions:
            answered_questions.add(selected_question)
            seen = False
    return selected_question, answered_questions


def display_question_and_options(current_question, current_options):
    """Clears the current screen, and displays the current question and the answer options in random order.  A dictionary is built to keep track of the order in which the options are presented by using key's corresponding to the order number provided for each option.
    """
    ordered_options = {}
    clear_terminal_window()
    print(current_question)
    for count, option in enumerate(current_options, 1):
        print("{}. {}".format(count,option))
        ordered_options[str(count)] = option
    return ordered_options
    
    
def get_user_answer(ordered_options):
    """Waits for the user to answer the question and rejects the answer if it is not one of the provided options.  The option number or the exact string for any of the displayed options is considered a valid answer choice.
    """
    valid = False
    while not valid:
        user_answer = input("Your answer: ")
        valid_choice = ordered_options.get(user_answer, None)
        if valid_choice:
            valid = True
        elif user_answer in ordered_options.values(): 
            valid = True
            valid_choice = user_answer
        else:
            print("{} is not an answer option. Please try again.".format(user_answer))
    return valid_choice


def is_answer_correct(user_answer, current_answer):
    """Compares the input user answer to the actual trivia answer"""
    if user_answer == current_answer:
        return True
    else:
        return False


def display_score(score, answered_questions=None, final=False):
    if final:
        return " Your final score is {} out of {} questions!".format(score, len(answered_questions))
    else:
        return "Your Score is now {}".format(score)
        

def update_score(score):
    """Increases the current score and displays the updated score"""
    clear_terminal_window()
    score += 1
    print("That's Correct!")
    current = display_score(score)
    print(current)
    return score
    
        
def reveal_correct_answer(current_question, current_answer):
    """Shows the correct answer and the current score"""
    clear_terminal_window()
    print("That's not it...")
    print("Q: {}".format(current_question))
    print("A: {}".format(current_answer))


def play_trivia_question(score, answered_questions, questions, question_options, question_answers):
    """Takes in all the current game data and:
    1. Chooses a question that has not been asked.
    2. Displays the trivia question.
    3. Takes in a user answer and check that it is valid.
    4. Compares the user's answer to the question's answer.
    5. Increments the score by one if correct, or reveals the correct answer if the answer is incorrect.
    """                                                   
    current, answered_questions = select_question(questions, answered_questions)
    current_question = questions[current]
    current_options = question_options[current]
    current_answer = question_answers[current]
    
    # The options are returned as a dictionary of their option number by order of display to the user.
    ordered_options = display_question_and_options(current_question,current_options)
    user_answer = get_user_answer(ordered_options)
    correct = is_answer_correct(user_answer, current_answer)
    if correct:
        score = update_score(score)
    else:
        reveal_correct_answer(current_question, current_answer)
    return score, answered_questions

    
def is_user_playing_again():
    """Asks if the user wants to play again by asking """
    choice = input("Would you like to play another round with this question bank? [Y/anything else]: ")
    if choice == "Y":
        return True
    else:
        return False


def play_game():
    """Holds game logic and continues question asking and answering until the first of the following conditions is met:
        1) 10 questions are answered
        2) All available questions are answered
        3) The game is exited with CTRL+C or Delete

        At game end, the current score is provided.  If condition 1 or 2 were reached, the player is asked if they would like to play again.  If not, the game exits.
    """
    new_game = True
    try:
        if new_game:
            explain_game()
            new_game = False
        playing = True
        while playing:
            # Game is initialized by validating the input file, building the 'question bank' and initializing the score and 
            # the answered questions.
            input_file = get_input_file()
            questions, question_options, question_answers = process_question_data(input_file)
            score = 0
            answered_questions = set()
            final_score_message = display_score(score, answered_questions, True)
            while not is_game_end(questions, answered_questions):
                score, answered_questions = play_trivia_question(score, answered_questions, questions, question_options, question_answers)                                 
                pause_for_user()
                # A final answer message is made in case this is 
                # the last question to answer or if there is a
                # KeyboardInterupt used to exit the game.
                final_score_message = display_score(score, answered_questions, True)
            print(final_score_message)
            playing = is_user_playing_again()    
    except KeyboardInterrupt:
        # If a round is exited prematurely, the current score is displayed.
        if not new_game:
            print("")
            print(final_score_message)
    except Exception as e:
        if hasattr(e, "message"):
            print(e.message)

    # exit() # remove when not testing


play_game()