# DECMOL
Tool for the discovery of process model using Model Learning Algorithms starting from an event log (in xes format)
## Features
It is possible to do different tasks with DECMOL, the major are: 
- Splitting the log into positive traces and negative traces 
This feature allows us to create the files that are needed to execute the model learning algorithms. In particular, given as input a file xes returns four files: alphabet.txt, positive.txt, negative1.txt, negative2.txt and negative3.txt. 
- Calculation of precision 
This option allows us to calculate the precision by taking as input the algorithm that generated the automaton, the automaton itself, the positive examples, and finally the parameter k that indicates the size of the substrings that we want to take into account.  
- Computing the generalization
This feature computes the generalization, in particular to perform this calculation it is needed in input the sets of positive and negative examples and the parameter N that indicates the number of sublogs that we want to use. Moreover, if the two sets are not specified, positive.txt and negative3.txt are selected by default. 

## Installation
Use the package manager pip to install project dependencies 
```bash
pip3 install -r requirements.txt
```
## Usage
The tool provides different features. Using the following command is possible to obtain a menu to select what you want to do.
```python
python3 main.py -h
```