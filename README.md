# Tandem Challenge 
#### Katerina Kossler's Submission for Tandem's 2021 Software Engineering Apprenticeship

### Instructions:
- System Dependencies: Python 3.9.0, (pip 20.2.4)
- Other requirements: Stored in a requirements.txt
  ```
  pip install -r requirements.txt
  ```
- Running the application: 
  1. Run the game by navigating into the game_folder 
    (Move in any custom JSON file(s) of questions you want to play with)
2. Install all requirements
3. Run the following (note - your version of Python 3.9.0 may be aliased as 'python'):
```
python3 game.py [JSON file of questions (optional)]
```
like the following options:
```
python3 game.py
python3 game.py Apprentice_TandemFor400_Data.json
python3 game.py more_questions.json
```
3. Play through by typing your answer as the option number or the full option test.
4. Submit your selection with enter.
5. Play to the first of 10 questions or all the questions available.
6. Play as many rounds as you want.
7. Exit at any time using Ctrl+C.

### Notes
##### MVP:
- [X] Process JSON File: need to parse, store, validate (num of Q and options for each Q)
- [X] Select current question
- [X] Score keeping / update score
- [X] Determine game state (question number and score)
- [X] Validate user selection / input
- [X] Check the selected answer
- [X] Provide end of game score and option to replay with current input set
- [ ] Add unit testing to the key functions.
##### Additional Features:
- [X] Add question class (and TriviaRound and Game classes)
- [X] Reconfigure how questions are randomized / reused (between rounds)
- [X] Add coloring for the game summary, and incorrect and correct answers

### Problem Scope
#### Tandem for 400!
- Create an application to improve a user's trivia skills by displaying multiple-choice trivia questions to answer.

- MVP:
  1. player can view: the question(s), 
  2. the answer choices, 
  3. the correct answer upon submission, 
  4. and their score
  4. can be a UI, command-line-tool, etc 

- Key Concepts to Demonstrate:
  1. Arrays and Loops
  2. Data Manipulation
  3. Parsing JSON
  4. (Not Required) Testing Methodologies

- Baseline Assumptions:
  1. A round of trivia has 10 Questions
  2. All questions are multiple-choice questions
  3. Your score does not need to update in real time
  4. Results can update on form submit, button click, or any other interaction
  5. Trivia data (questions, correct and incorrect answers) is provided via a JSON file.
  
- Acceptance Criteria
  1. A user can view questions.
  2. Questions with their multiple choice options must be displayed one at a time.
  3. Questions should not repeat in a round.
  4. A user can select only 1 answer out of the 4 possible answers.
  5. The correct answer must be revealed after a user has submitted their answer
  6. A user can see the score they received at the end of the round

#### Submission Details
- application window will close Sunday,
November 1 11:59PM CST
- Please include a link to your submission in your application (we do have a
question for this). 
- You are welcome to put your code challenge submission in Github, Bitbucket, or a public source control service of your choosing.
- Please exclude any binaries or dependencies that can be built or resolved via a
package manager (remember to .gitignore those node_modules!).
- Your submission must include instructions for how to run your code. 
- You must also list any system dependencies (e.g. Ruby 2.3, Erlang runtime, JDK8, etc).