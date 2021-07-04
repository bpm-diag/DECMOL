from pythomata import SimpleDFA
from graphviz import Digraph
import sys

def AutomataChar(file):
	fp = open(file,"r")
	lines = fp.readlines()
	states = 0
	transitions = 0
	initial_state = ""
	for line in lines:
		if "[shape" in line:
			states +=1
		elif "[label" in line:
			if "__start" in line: 
				continue
			transitions +=1
		elif "__start0 ->" in line:
			v = (line.split(' ', 2)[2])[1:].strip()
			initial_state = v[:-1]
	fp.close()
	print("Number of states : ",str(states),"Number of transitions ",str(transitions))
	

def AutomataDot(file):
	states = set()
	fp = open(file,"r")
	lines = fp.readlines()
	transitions = 0
	for line in lines:
		if "[label" in line:
			v = line.strip().split(' ', 2)
			s1 = int((v[0]))
			s2 = int((v[2])[:v[2].find("[")].strip())
			label = (v[2])[v[2].find("=")+2: v[2].find("]")-1].lower().replace(" ","")
			states.add(s1)
			states.add(s2)
			v = label.split('\\n')
			for i in v:
				transitions+=1	
	fp.close()
	print("Number of states : ",(len(states),"Number of transitions ",(transitions)))
if __name__ == "__main__":
	auto = sys.argv[1]
	if ".dot" in auto:
		AutomataDot(auto)
	else:
		AutomataChar(auto)
		
