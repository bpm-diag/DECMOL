# DECMOL
Tool for the discovery of process model using Model Learning Algorithms starting from an event log (in xes format)
## Features
It is possible to do different tasks with DECMOL, the major are: 
- Splitting the log into positive traces and negative traces <br />
This feature allows us to create the files that are needed to execute the model learning algorithms. In particular, given as input a file xes returns four files: alphabet.txt, positive.txt, negative1.txt, negative2.txt and negative3.txt. 
- Calculation of precision <br />
This option allows us to calculate the precision by taking as input the algorithm that generated the automaton, the automaton itself, the positive examples, and finally the parameter k that indicates the size of the substrings that we want to take into account.  
- Computing the generalization <br />
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
## How to Run 
1. **Pre-Processing:** python3 main.py -e <event-log.xes>
* input:
	* <event-log.xes>
* output:
	* <alphabet.txt>: 
	* <positive.txt>: 
	* <negative1.txt>: 
	* <negative2.txt>: 
	* <negative3.txt>: 
2. **Build Automaton:** python3 main.py -a <RPNI | EDSM | MDL | LSTAR> <alphabet.txt> <positive.txt> <negative.txt>
* input: 
	* <RPNI | EDSM | MDL | LSTAR>
	* <alphabet.txt>
	* <positive.txt>
	* <negative.txt>
* output: 
	* <automaton.txt>:
	* <time.txt>:
3. **Compute Precision:** python3 main.py -p <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <automaton.txt | automaton.dot> <positive.txt> <alphabet.txt> <K>
* input:
	* <RPNI | EDSM | MDL | LSTAR> 
	* <positive.txt>
	* <alphabet.txt>
	* <K>:
* output:
	* <precision.txt>
4. **Compute Generalization** python3 main.py -g <positive.txt> <negative> <N>
* input:
	* <positive.txt>
	* <negative.txt>
	* <N>
* output:
	* <generalization.txt>