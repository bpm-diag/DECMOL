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
* _input_:
	* <event-log.xes>
* _output_:
	* <alphabet.txt>: it stores in each line the alphabet symbols that come from the event log. 
	* <positive.txt>: it collects 70% of the traces in the event log 
	* <negative1.txt>: it represents the 10% of the traces in the event log 
	* <negative2.txt>: it stores 20% of the traces in the event log
	* <negative3.txt>: it memorizes 30% of the traces in the event log
2. **Build Automaton:** python3 main.py -a <RPNI | EDSM | MDL | LSTAR> <alphabet.txt> <positive.txt> <negative.txt>
* _input_: 
	* <RPNI | EDSM | MDL | LSTAR>
	* <alphabet.txt> 
	* <positive.txt>
	* <negative.txt>
* _output_: 
	* <automaton.txt>: it represents the automaton discovered through a model learning algorithm 
	* <time.txt>: in this file is memorized the time needed by the chosen algorithm to compute the automaton
3. **Compute Precision:** python3 main.py -p <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <automaton.txt | automaton.dot> <positive.txt> <alphabet.txt> &lt;K&gt;  
* _input_:
	* <RPNI | EDSM | MDL | LSTAR> 
	* <positive.txt>
	* <alphabet.txt>
	* &lt;K&gt; : it identifies the length of the substrings that you want to take into account to describe the behavior of the log and automaton.
* _output_:
	* <precision.txt>: in this file is stored the value of the precision for the behaviors that have a length from 2 to k.
4. **Compute Generalization** python3 main.py -g <positive.txt> <negative | negative2.txt | negative3.txt> &lt;N&gt; 
* _input_:
	* <positive.txt>
	* <negative1.txt | negative2.txt | negative3.txt>
	* &lt;N&gt;: it is the number of sublogs that you want to use for the calculation of the generalization
* _output_:
	* <generalization.txt>: in this file is stored the value of the generalization, in particular, you have three different values (one for each automaton discovered using the different amount of negative traces: 10%, 20%, and 30%)