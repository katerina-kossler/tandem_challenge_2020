import sys
from os import name as os_name, system as os_system
from json import load
from exceptions import InputFileError
from random import shuffle
import argparse
from colorama import init #https://pypi.org/project/colorama/
from termcolor import cprint #https://pypi.org/project/termcolor/
init() # to have termcolor supported on Windows

def clear_terminal_window():
    """Clears the terminal for clarity based on the os name.  Windows uses a command of 'cls' while Mac and Linux use 'clear'."""
    if os_name == 'nt': 
        os_system('cls') 
    else: 
        os_system('clear')

class Question():
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer
          
    def ask(self):
        """Clears the current screen, and displays the current question and the answer options in random order.  A dictionary is built to keep track of the order in which the options are presented by using key's corresponding to the order number provided for each option.
        
        Waits for the user to answer the question and rejects the answer if it is not one of the provided options.  The option number or the exact string for any of the displayed options is considered a valid answer choice.
        """
        shuffle(self.options)
        clear_terminal_window()
        print(self.question)
        ordered_options = {}
        shuffle(self.options)
        for count, option in enumerate(self.options, 1):
            print("{}. {}".format(count,option))
            ordered_options[str(count)] = option

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
        
    def reveal_result(self, correct):
        if correct:
            cprint("Ding! Ding! That's Correct!","green")
            cprint("Q: {}".format(self.question),"green")
            cprint("A: {}".format(self.answer),"green")
        else:
            cprint("Oh, and that's a bad miss!","red")
            cprint("Q: {}".format(self.question),"red")
            cprint("A: {}".format(self.answer),"red")

class TriviaRound():
    def __init__(self, unused_questions, incorrect_questions=[], correct_questions=[]):
        self.unused_questions = unused_questions
        self.questions_to_ask = []
        self.incorrect_questions = incorrect_questions
        self.correct_questions = correct_questions
        self.score = 0
        
    def build_new_round(self):
        self.score = 0
        # add comments
        if len(self.incorrect_questions) >= 10:
            shuffle(self.incorrect_questions)
            while (len(self.questions_to_ask) < 10):
                self.questions_to_ask.append(self.incorrect_questions.pop())
        elif (len(self.unused_questions) + len(self.incorrect_questions)) >= 10:
            while self.incorrect_questions:
                self.questions_to_ask.append(self.incorrect_questions.pop()) 
            while len(self.questions_to_ask) < 10:    
                self.questions_to_ask.append(self.unused_questions.pop())
            shuffle(self.questions_to_ask)
        else:
            self.unused_questions.extend(self.incorrect_questions)
            self.incorrect_questions = []
            self.unused_questions.extend(self.correct_questions)
            self.correct_questions = []
            shuffle(self.unused_questions)
            while self.unused_questions or len(self.questions_to_ask) < 10:
                self.questions_to_ask.append(self.unused_questions.pop())
        
    def play_trivia_question(self):
        question = self.questions_to_ask.pop()
        user_answer = question.ask()
        if user_answer == question.answer:
            self.score += 1
            self.correct_questions.append(question)
            question.reveal_result(correct=True)
        else:
            self.incorrect_questions.append(question)
            question.reveal_result(correct=False)
    
    def get_score_message(self):
        return "Your final score is {} points!".format(self.score)
    
class Game():
    def __init__(self, input_file, question_key, incorrect_options_key, answer_key):
        self.question_key = question_key
        self.incorrect_options_key = incorrect_options_key
        self.answer_key = answer_key
        self.input_file = input_file
        self.scores = []
    
    def get_key(self, key, question, question_id):
        """Validates the current key for the question and returns its value."""
        if question.get(key, None):
            return question[key]
        else:
            raise InputFileError(key, question_id)

    def process_question_data(self):
        """Takes in a JSON file of questions in the format:
        {"question": "<QUESTION>",
        "incorrect": ["<INCORRECT_OPTION_1>", ..., "<INCORRECT_OPTION_X>"],
        "correct": "<CORRECT_OPTION>"}
        
        Validates and processes the data into a Question object with attributes of
        - the question (str)
        - all options (array of str)
        - the answer (str)
        """
        all_questions = []
        with open(self.input_file) as json_file:
            for current_number, current_question in enumerate(load(json_file),1):
                question = self.get_key(self.question_key,      
                                    current_question, 
                                    current_number)
                options = self.get_key(self.incorrect_options_key, 
                                    current_question, 
                                    current_number)
                answer = self.get_key(self.answer_key, 
                                    current_question, 
                                    current_number)
                options.append(answer)
                
                new_question = Question(question, options, answer)
                all_questions.append(new_question)
        return all_questions
        
    def pause_for_user(self):
        """Waits for user to hit enter to continue so they have time to review the current screen."""
        wait_message = "Hit enter when you are ready to continue. [ctrl+c to quit]"
        input(wait_message)

    def explain_game(self):
        """Outputs the basic gameplay for this trivia game"""
        cprint("""
        Welcome to the hottest new CLI game to hit your terminal!
         ______               __               ___              ____  ___   ___   __
        /_  __/___ _ ___  ___/ /___  __ _     / _/___   ____   / / / / _ \ / _ \ / /
         / /  / _ `// _ \/ _  // -_)/  ' \   / _// _ \ / __/  /_  _// // // // //_/ 
        /_/   \_,_//_//_/\_,_/ \__//_/_/_/  /_/  \___//_/      /_/  \___/ \___/(_)  
                                                                                    
        ""","blue")
        print("""
        Using the JSON file you passed in as an argument (or the default file 
        if you didn't provide one), we will build a randomized round of trivia
        for you to answer!
        
        Each round of trivia will consist of 10 questions (if possible).
        For each question, type in your selection and hit enter.
            
        Leave at any point using Ctrl+C. 
        """)
        self.pause_for_user()

    def play_game(self):
        """Holds game logic and continues question asking and answering until the first of the following conditions is met:
            1) 10 questions are answered
            2) All available questions are answered
            3) The game is exited with CTRL+C or Delete

        At game end, the current score is provided.  If condition 1 or 2 were reached, 
        the player is asked if they would like to play again.  If not, the game exits.
        """
        # need to rehandle how I show the ValueError / InputFileError to the user
        questions = self.process_question_data()
        trivia_round = TriviaRound(questions)
        try:
            self.explain_game()
            playing = True
            while playing:
                trivia_round.build_new_round()
                final_score_message = trivia_round.get_score_message()
                
                while len(trivia_round.questions_to_ask) > 0:
                    trivia_round.play_trivia_question()
                    self.pause_for_user()               
                    final_score_message = trivia_round.get_score_message()
                
                print(final_score_message)
                self.scores.append(trivia_round.score)
                
                choice = input("Would you like to play another round? [Y/anything else]: ")
                if choice == "Y":
                    trivia_round.build_new_round()
                else:
                    playing = False
                    
            print("Here were your scores from this game:")
            for score in self.scores:
                print(score)
            cprint("Have a good one!","blue")
        
        except KeyboardInterrupt:
            # If a round is exited prematurely, the current score is displayed.
            print("")
            print(final_score_message)

# to do:

# add unit tests
# fix comments


if __name__ == "__main__":
    
    input_parser = argparse.ArgumentParser(
        description="Answer a random subset of trivia questions from an input JSON file."
    )
    input_parser.add_argument("--questions_file",
                              type=argparse.FileType("r"),
                              help="Enter the JSON file of questions you want to use here (default: 'Apprentice_TandemFor400_Data.json').",
                              default="Apprentice_TandemFor400_Data.json",
                              metavar="JSONFILE")
    input_parser.add_argument("--question",
                              type=str,
                              help="The 'question' key for all questions in the JSON file (default: 'question').",
                              default="question")
    input_parser.add_argument("--incorrect_options",
                              type=str,
                              help="The 'incorrect options' key for all questions in the JSON file (default: 'incorrect').",
                              default="incorrect")
    input_parser.add_argument("--answer",
                              type=str,
                              help="The 'answer' key for all questions in the JSON file (default: 'correct').",
                              default="correct")
    args = input_parser.parse_args()

    if args.questions_file:
        if ".json" in args.questions_file.name:
            try:
                load(args.questions_file)
            except Exception as e:
                print('hi')
                raise argparse.ArgumentTypeError(
                    "Input file '{}' is not a valid JSON file. Error: {}".format(
                        args.questions_file.name,
                        e
                    )
                )
    game = Game(input_file=args.questions_file.name,
                question_key=args.question,
                incorrect_options_key=args.incorrect_options,
                answer_key=args.answer)
    game.play_game()