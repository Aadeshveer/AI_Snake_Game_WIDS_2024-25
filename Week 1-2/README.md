# AI_Snake_Game_WIDS_2024-25

## Description:
##### The attatched file(Week2_submission.ipynb) is my submission for week 2 assignment. It is a machine learning code which
##### 1) Imports required libraries
##### 2) Ensures cuda service if available
##### 3) Downloads/uses MNIST dataset
##### 4) Uses pytorch neural network to train itself
##### 5) Calculates accuracy it achieves after training

## Hyper parameters:
##### Number of epochs    = 10
##### Batch_size of data  = 50
##### Learning rate       = 0.001
##### Expected accuracy   = ~99.5 %

## Structure of neural network:
#### 3 fully connected layers:
##### First layer has input size of 784(=28*28) to read the flattened form of picture and outputs 128 data points to next layer after passing through activation function(ReLu). The second layer inputs the 128 data points and passes 64 to next after passing through the activation function(ReLu). Final layer takes 64 data points and returns a digit(0 to 9).
