# AI_Snake_Game_WIDS_2024-25

## Description:
##### The attatched files create an AI learning system which plays the snake game. AIgame.py is the code for the game made using pygame, that gives the control to the AI agent playing the game. Agent.py is the file that runs as the AI agent which moves using AIgame.py, chooses actions using the AI model and provides us the output of its performance. model.py is a pytorch implemented file that holds the neural network used by the AI agent to select move based on state and train present model. Helper.py is a matplotlib implemented file that allows Agent to give us real time status of performance of the model over time. The "resources" folder includes various files to aid graphics in the game.

## Parameters(can be altered from AIgame.py):
##### Background color    = (221, 227, 52)    line 20
##### Text color          = (0, 0, 0)         line 19
##### Block size          = 20 px             line 23
##### Screen size         = 640x480 px        line 28 (w and h)
##### Speed               = 80 units          line 24

## How to run:
##### Download all files in the repository in a common location and run Agent.py.

## AI model details:
##### The AI model used has 3 layers:
##### First input layer has 11 inputs(all binary ie 0 or 1, first 3 tell if snake has danger ahead, left and/or right, next 4 for the direction snake is facing in, and last 4 for relative direction of food.
##### Hidden layer has a size of 256.
##### Output is a tensor of size 3 from whom a move is selected based on index of largest number(0=striaght, 1=right, 2=left)

## Hyper Parameters(can be altered from Agent.py):
##### Hidden layer size                          = 256                                         line 20
##### Learning rare                              = 0.001                                       line 11
##### Batch size for long term training          = 1000                                        line 10
##### Max states to store for long term training = 100000                                      line 9
##### Discount rate(gamma)                       = 0.9                                         line 18
##### Exploration ratio                          = (80 - number of games played) in 200 moves  line 26 and 28

### This project was made as a submission to Winter in Data Science at IIT Bombay under the mentorship of Saksham Saharia and Prabhav Khandelwal. The project is a derivative of same made by Patrick Loeber availible at https://github.com/patrickloeber/snake-ai-pytorch.
