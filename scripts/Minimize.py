from pythomata import SimpleDFA
from graphviz import Digraph
import sys, os

def dfaminimized(folder,al,automaton,i,typ,j):
	#creation alphabet
	alphabet = set()
	fp = open(al,"r")
	lines = fp.readlines()
	for line in lines:
		alphabet.add(line.strip())

	#my automaton to pythomata automaton
	states = set()
	initial_state = "";
	accepting_states = set()
	fp = open(folder+automaton+".txt","r")
	lines = fp.readlines()
	transition_function = {}
	for line in lines:
		if "[shape" in line:
			v = line.split(' ', 2)
			s1 = (v[0].strip())[1:]
			s2 = (v[1])[8:len(v[1])-1]
			if "doublecircle" == s2:
				accepting_states.add(s1)
			states.add(s1)
		elif "[label" in line:
			if "__start" in line: 
				continue
			v = line.split(' ', 2)
			s1 = (v[0].strip())[1:]
			s2 = (v[2])[1:v[2].find("[")].strip()
			label = (v[2])[v[2].find("=")+2: v[2].find("]")-1]

			if s1 in transition_function:
				l = transition_function[s1]
				l[label] = s2
			else:
				l={}
				l[label] = s2
				transition_function[s1] = l
		elif "__start0 ->" in line:
			v = (line.split(' ', 2)[2])[1:].strip()
			initial_state = v[:-1]
	
	dfa = SimpleDFA(states,alphabet,initial_state,accepting_states,transition_function)
	graph = dfa.minimize().to_graphviz()
	if(typ=="MDL"):
		graph.save(folder+os.sep+str(i)+os.sep+typ+os.sep+"dfa_minimized"+os.sep+"automaton")
	else:
		graph.save(folder+os.sep+str(i)+os.sep+typ+os.sep+"dfa_minimized"+os.sep+"automaton"+str(j))

if __name__ == "__main__":
	k = int(sys.argv[1:][0])
	alg = sys.argv[1:][1]
	alphabet = sys.argv[1:][2]
	folder = "generalization"+os.sep
	if alg == "MDL":
		for i in range(k):
			automaton = str(i)+os.sep+"MDL"+os.sep+"automaton"
			dfaminimized(folder,alphabet,automaton,i,"MDL",0)
	else:
		for i in range(k):
			for j in range(1, 4):
				automaton = str(i)+os.sep+alg+os.sep+"automaton"+str(j)
				dfaminimized(folder,alphabet,automaton,i,alg,j)
			