from unittest.mock import patch
from unittest import TestCase, mock

# unittests
# functions not covered:
# clear_terminal_window()
# Question.revealResult()
# TriviaRound.get_score_message()
# Game.explain_game(), Game.pause_for_user()

class TestProcessQuestionData(TestCase):
    question1 = json()
    def test_empty_question(self):
        self.assertRaises(question1.)
    question2 = Question(question='Test: ', options=[], answer='C')

    question3 = Question(question='Test: ', options=['A', 'B', 'C', 'D'], answer='')