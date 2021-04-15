from pythomata import SimpleDFA
from graphviz import Digraph
from itertools import combinations 
import sys, os
#To get all automaton states : automaton.states 
#To get the initial state : automaton.initial_state
#To get the automaton accepting states : automaton.accepting_states
#To get all transitions: automaton.get_transitions()
def myDFS(trans_dict,start,length,paths,pathset,path=[],st=""): 
	    path=path+[start] 
	    if len(path)==length:
	    	#print(st)
	    	pathset.add(st)
	    	paths.append(path)

	    else:
	    	if not start in trans_dict:
	    		return
	    	for node in trans_dict[start]:
	    		st+=node[1]
	    		myDFS(trans_dict,node[0],length,paths,pathset,path,st)
	    		st=st[:-len(node[1])]

def precisionALL(automaton, positive, alphabet, length, K, reportfile):

	def precision(automaton, positive, alph, length, K, reportfile):
		
		report = open(reportfile,"a")
		report.write("Precision with K = "+str(K)+"\n")
		alphabet = set()
		fp = open(alph,"r")
		lines = fp.readlines()
		for line in lines:
			alphabet.add(line.strip())

		#my automaton to pythomata automaton
		states = set()
		initial_state = "";
		accepting_states = set()
		fp = open(automaton,"r")
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
		fp.close()

		dfa = SimpleDFA(states,alphabet,initial_state,accepting_states,transition_function)
		dfa_minimized = dfa.minimize()
		dfa_trimmed = dfa_minimized.trim()

		transitions = dfa_trimmed.get_transitions()
		
		trans = {}
		for i in transitions:
			if i[0] in trans:
				l = trans[i[0]]
				l.append((i[2],i[1]))
			else: 
				trans[i[0]] = [(i[2],i[1])]

		paths = []
		pathset = set()
		
		for a in trans:
			myDFS(trans,a,length,paths,pathset)
		
		
		report.write("Number paths automaton "+str(len(paths))+"\n")
		report.write("Number different string automaton "+str(len(pathset))+"\n")

		fp = open(positive,"r")
		lines = fp.readlines()
		
		logset = set()
		for line in lines:
			line = line.strip()
			line = line.split(" ")
			if(len(line) == K):
				el = ""
				for i in line:
					el += i
				logset.add(el)
			else:
				for i in range(len(line) - K + 1): 
					sum = ""
					for j in range(i, K + i): 
						sum += line[j] 
					logset.add(sum)
		fp.close()

		report.write("Number substrings log "+str(len(logset))+"\n")
		report.write("Precision "+str(1-((len(pathset)-len(logset))/len(pathset)))+"\n\n")

	precision(automaton, positive, alphabet, length, K, reportfile)

def precisionDOT(automaton, positive, length, K, reportfile):
	def precision(automaton, positive, length, K, reportfile):
		report = open(reportfile,"a")
		report.write("Precision automaton DeclareMiner:  with K = "+str(K)+"\n")

		states = set()
		initial_state = "";
		accepting_states = set()
		fp = open(automaton,"r")
		lines = fp.readlines()
		transition_function = {}
		for line in lines:
			if "[label" in line:
				v = line.strip().split(' ', 2)
				s1 = int((v[0]))
				s2 = int((v[2])[:v[2].find("[")].strip())
				label = (v[2])[v[2].find("=")+2: v[2].find("]")-1].lower().replace(" ","")
				
				v = label.split('\\n')
				for i in v:
					if s1 in transition_function:
						l = transition_function[s1]
						l.append((s2,i))
					else:
						transition_function[s1] = [(s2,i)]
		
		#print(transition_function)
		fp.close()
		paths = []
		pathset = set()
		for a in transition_function:
			myDFS(transition_function,a,length,paths,pathset)
		
		
		report.write("Number paths automaton "+str(len(paths))+"\n")
		report.write("Number different string automaton "+str(len(pathset))+"\n")

		fp = open(positive,"r")
		lines = fp.readlines()
		
		logset = set()
		for line in lines:
			line = line.strip()
			line = line.split(" ")
			if(len(line) == K):
				el = ""
				for i in line:
					el += i
				logset.add(el)
			else:
				for i in range(len(line) - K + 1): 
					sum = ""
					for j in range(i, K + i): 
						sum += line[j] 
					logset.add(sum)
		fp.close()
		report.write("Number substrings log "+str(len(logset))+"\n")
		report.write("Precision "+str(1-((len(pathset)-len(logset))/len(pathset)))+"\n\n")
		
	precision(automaton, positive, length, K, reportfile)	

if __name__ == "__main__":
	i = sys.argv[1:]
	automaton = i[0]
	positive = i[1]
	alphabet = i[2]
	typ = i[3]
	parameterk = i[4]
	print(alphabet)
	if typ == "MDL" or typ == "RPNI" or typ== "EDSM" or typ == "LSTAR":
		aut = automaton[automaton.rfind(os.sep)+1:]

		reportfile = "result"+os.sep+"precision_report_"+aut
		report = open(reportfile,"w")
		report.write("Precision report using "+typ+" algorithm for the discovery task\n")
		report.close()
		for i in range(2, int(parameterk)+1):
			length = i+1
			K = i
			precisionALL(automaton, positive, alphabet, length, K, reportfile)
	elif typ == "DeclareMiner":
		reportfile = "result"+os.sep+"precision_report"+"_"+automaton
		report = open(reportfile,"w")
		report.write("Precision report using "+typ+" algorithm for the discovery task\n")
		report.close()
		for i in range(2, int(parameterk)+1):
			length = i+1
			K = i
			precisionDOT(automaton, positive, length, K, reportfile)



