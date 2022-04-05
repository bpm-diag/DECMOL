# DECMOL
Tool for the discovery of process model using Model Learning Algorithms (RPNI, EDSM, MDL and LSTAR) starting from an event log (in xes format)
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
1. **Pre-Processing:** python3 main.py -e <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <EventLog.xes>
* _input_:
	* <RPNI | EDSM | MDL | LSTAR | DeclareMiner>
	* <EventLog.xes>
* _output_:
	* <alphabet.txt>: it stores in each line the alphabet symbols that come from the event log. 
	* <positive.txt>: it collects 70% of the traces in the event log 
	* <negative1.txt>: it represents the 10% of the traces in the event log 
	* <negative2.txt>: it stores 20% of the traces in the event log
	* <negative3.txt>: it memorizes 30% of the traces in the event log
Whether MDL or DeclareMiner is selected as algorithm the output is:
	* <alphabet.txt>: it stores in each line the alphabet symbols that come from the event log. 
	* <positive.txt>: it collects 100% of the traces in the event log 
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
	* <precision_with_Hungarian_Algorithm.txt>: in this file is stored the value of the precision for the behaviors that have a length from 2 to k using Hungarian Algorithm.
4. **Compute Generalization** python3 main.py -g <RPNI | EDSM | MDL | LSTAR> <positive.txt> <negative.txt> &lt;N&gt; &lt;K&gt; 
* _input_:
	* <RPNI | EDSM | MDL | LSTAR> 
	* <positive.txt>
	* <negative1.txt | negative2.txt | negative3.txt> it is possible to select the negative file that you want.
	* &lt;N&gt; : it is the number of sublogs that you want to use for the calculation of the generalization
	* &lt;K&gt; : it represents the length of the behaviours that will be used for the calculation of the fitness through the Hungarian Algorithm.
Whether MDL is selected like algorithm the negative file does not have to be specified. Moreover is possible to select just the algorithm, N and K parameters, and the generalization is computed considering the positive.txt and negative3.txt (if it is needed) files inside preprocessing folder.
* _output_:
	* <generalization.txt>: in this file is stored the value of the generalization. In particular, it will contain a value for each length of the behaviours you want to consider and, where possible, also based on the number of negative traces for each sublog. 
5. **Compute Generalization for DeclareMiner algorithm** python3 main.py -d <positive.txt> &lt;N&gt; &lt;K&gt; <automaton1.dot> ... <automatonN> 
* _input_:
	*<positive.txt>
	*&lt;N&gt; : it is the number of sublogs that you want to use for the calculation of the generalization
	*&lt;K&gt; : it represents the length of the behaviours that will be used for the calculation of the fitness through the Hungarian Algorithm.
	*<automatoni.dot> : it represents the automaton discovered by the DeclareMiner algorithm for the i-th sublog
6. **All automated functionality** python3 main -c <RPNI | EDSM | MDL | LSTAR> &lt;K1&gt; &lt;N&gt; &lt;K2&gt; <EventLog> 
* _input_:
	* <RPNI | EDSM | MDL | LSTAR> 
	* &lt;K1&gt; : it identifies the length of the substrings that you want to take into account to describe the behavior of the log and automaton for the precision calculation.
	* &lt;N&gt; : it is the number of sublogs that you want to use for the calculation of the generalization
	* &lt;K2&gt; : it represents the length of the behaviours that will be used for the calculation of the fitness through the Hungarian Algorithm.
Whether it is chosen to use one of the algorithms that uses the negative traces is selected the file with 30% of negative traces
	
## New Metrics
It is possible to compute the metrics based on the Markovian abstraction using the files in the *new_metrics* folder. For (positive) precision run
```python
python3 precision.py pos_log.xes process.dot k
```
where pos_log.xes is the positive log in xes format used for learning the model in process.dot.
For the negative precision run
```python
python3 neg_precision.py neg_log.xes process.dot alphabet.txt k
```
where neg_log.xes is the negative log used for learning the model in process.dot and alphabet.txt is the file obtained during the preprocessing (note that the alphabet is now required since the negative precision involves the computation of the complement of a DFA)
	
Analougly, for computing the recall.

For computing both positive and negative recall just run
```python
python3 generalization.py pos_log.xes neg_log.xes k h
```	
where k is the order of the Markovian abstraction and h is the number of sublogs. Note that for computing the generalization ModelLearning.jar must be in the same folder.

For splitting the original log in positive and negative run
```python
python3 split.py <log_name> <log_folder>
```
where <log_name> is the filename of the xes log and <log_folder> the path to the folder containing <log_name>. Remember to include the path separator at the end of <log_folder>. After the execution of this script four different files will be created under the <log_folder> directory:
	
	1. <log_name>_positive.txt
	
	2. <log_name>_negative.txt
	
	3. <log_name>_positive.xes
	
	4. <log_name>_negative.xes
 
First two files will be exploited by ModelLearning.jar for the computation of the automaton, while the last two by the new metrics scripts.
