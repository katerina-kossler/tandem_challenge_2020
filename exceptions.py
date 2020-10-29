# Custom exceptions in this file are to be used for supporting the validation of game.py .


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

class InputArgumentsException(Exception):
    """Exception raised by errors in the arguments provided to the game."""
    def __init__(self):
        self.message = "Too many arguments provided. Provide the game with one JSON file of questions."
        super().__init__(self.message)