# Tandem Challenge 
#### Katerina Kossler's Coding Challenge for Tandem's 2021 Software Engineering Apprenticeship

### Problem Scope
#### Tandem for 400!
##### Create an application to improve a user's trivia skills by displaying multiple-choice trivia questions to answer

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
- You must
also list any system dependencies (e.g. Ruby 2.3, Erlang runtime, JDK8, etc).

### Notes
#### Plan:
- MVP:
  1. CL-game built using Python.
  2. User types the selected answer from the available options and hits enter to submit the selection. 
  3. Game proceeds until 10 Q have been answered. 
  4. Application that can ran locally (can include JSON file in opening the application & exit with CTRL+C). 
  5. Key functions are covered by unit tests.
  
- Additional Features:
  1. Simple UI: Using Flask / Jinja / React in some capacity.
  2. Questions are randomly displayed and the user clicks their selection. After clicking, the correct answer is revealed, score is updated. 
  3. Click move on to next question. 
  4. Once round is over, final score is shown along with condensed view of seen questions and their answers (maybe conditional coloring if the question was correct or not).
  5. Tracks player information either while running or with a simple SQL DB. Could store player's past scores and successful input files - like a nice arcade game).
  6. Function to upload new Q/A JSON file (should need validation to play with anything other than the default file).
  
#### To-do list:
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
- [ ] 
- [ ]
- [ ]
- [ ]


### Instructions
- Running the application: 
1. Run the game by navigating into the game_folder (along with a JSON file of questions if you have custom ones you want to run)
2. Run the following:
```
python3 game.py [file.json - optional]
```
3. Play through by typing your answers and submitting by hitting enter.
4. Exit at any time using Ctrl+C.
