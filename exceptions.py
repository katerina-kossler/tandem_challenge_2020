# Custom exceptions in this file are to be used for supporting the validation of game.py .


class InputFileKeyError(Exception):
    """Exception raised for Key errors in the input file.
    
    Attributes: 
    - key: the JSON key expected to be found in the input file
    - question_id: the current JSON object that the is not found for
    """
    def __init__(self, key, question_id):
        self.key = key
        self.question_id = question_id
        self.message = "'{}' key is missing from question {}".format(key, question_id)
        super().__init__(self.message)
        
class InputFileValueError(Exception):
    """Exception raised for empty Values in the input file.
    
    Attributes: 
    - key: the JSON key expected to be found in the input file
    - question_id: the current JSON object that the is not found for
    """
    def __init__(self, key, question_id):
        self.value = key
        self.question_id = question_id
        self.message = "'{}' value is empty in question {}".format(key, question_id)
        super().__init__(self.message)