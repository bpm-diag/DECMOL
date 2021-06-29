from pythomata import SimpleDFA
from graphviz import Digraph
from itertools import combinations
from Levenshtein import *
import sys, subprocess, os, getopt

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
	    		st+=node[1]+" "
	    		myDFS(trans_dict,node[0],length,paths,pathset,path,st)
	    		st=st[:-len(node[1])-1]

def precisionHung(automaton, positive, alphabet, length, K, reportfile):
	def precision(automaton, positive, alph, length, K, reportfile):
		reportf = open(reportfile,"a")
		if not os.path.exists("preprocessing"):
			os.mkdir("preprocessing")  
		report = open("preprocessing"+os.sep+"matrix.txt","w")
		reportf.write("Precision with K = "+str(K)+"\n")
		reportf.close()
		alphabet = set()
		fp = open(alph,"r")
		lines = fp.readlines()
		for line in lines:
			alphabet.add(line.strip())

		#hash table --> key = event, value = alphabet
		mapping = dict()
		if len(alphabet) > 256:
			print("Error, alphabet too big.")
			exit(1)
		else:
			x = 0
			for i in alphabet:
				mapping[i] = chr(x)
				"""
				x+=1
				if(x==123):
					x=65
				"""
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

		fp = open(positive,"r")
		lines = fp.readlines()
		
		logset = set()
		for line in lines:
			line = line.strip()
			line = line.split(" ")
			if(len(line) == K):
				el = ""
				for i in line:
					el += i+" "
				logset.add(el)
			else:
				for i in range(len(line) - K + 1): 
					sum = ""
					for j in range(i, K + i): 
						sum += line[j]+" "
					logset.add(sum)
		fp.close()

		report.write(str(len(pathset))+"\n")
		report.write(str(len(logset))+"\n")

		#applying the mapping with hash map
		abcautomaton = set()
		for k in pathset:
			k = k.strip().split(" ")
			st = ""
			for el in k:
				st += mapping[el]
			abcautomaton.add(st)

		abclog = set()
		for k in logset:
			k = k.strip().split(" ")
			st = ""
			for el in k:
				st += mapping[el]
			abclog.add(st)

		#matrix = [[]]
		#row = 0
		for i in abcautomaton:
			for j in abclog:
				#matrix[row].append(distance(i,j))
				report.write(str(distance(i,j))+" ")
			#matrix.append([])
			report.write("\n")
			#row+=1
		report.close()
		subprocess.call(["java","-Xms1g", "-Xmx40g", "-jar", "scripts"+os.sep+"Hungarian.jar", "preprocessing"+os.sep+"matrix.txt", reportfile])

	precision(automaton, positive, alphabet, length, K, reportfile)

def precisionDOT(automaton, alph, positive, length, K, reportfile):
	def prec(automaton, alph, positive, length, K, reportfile):
		reportf = open(reportfile,"a")
		reportf.write("Precision automaton DeclareMiner:  with K = "+str(K)+"\n")
		reportf.close()
		if not os.path.exists("preprocessing"):
			os.mkdir("preprocessing")  
		report = open("preprocessing"+os.sep+"matrix.txt","w")

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
		
		fp = open(positive,"r")
		lines = fp.readlines()
		
		logset = set()
		for line in lines:
			line = line.strip()
			line = line.split(" ")
			if(len(line) == K):
				el = ""
				for i in line:
					el += i+" "
				logset.add(el)
			else:
				for i in range(len(line) - K + 1): 
					sum = ""
					for j in range(i, K + i): 
						sum += line[j]+" "
					logset.add(sum)
		fp.close()
		
		report.write(str(len(pathset))+"\n")
		report.write(str(len(logset))+"\n")

		alphabet = set()
		fp = open(alph,"r")
		lines = fp.readlines()
		for line in lines:
			alphabet.add(line.strip())

		mapping = dict()
		if len(alphabet) > 256:
			print("Error, alphabet too big.")
			exit(1)
		else:
			x = 0
			for i in alphabet:
				mapping[i] = chr(x)

		#applying the mapping with hash map
		abcautomaton = set()
		for k in pathset:
			k = k.strip().split(" ")
			st = ""
			for el in k:
				st += mapping[el]
			abcautomaton.add(st)

		abclog = set()
		for k in logset:
			k = k.strip().split(" ")
			st = ""
			for el in k:
				st += mapping[el]
			abclog.add(st)

		#matrix = [[]]
		#row = 0
		for i in abcautomaton:
			for j in abclog:
				#matrix[row].append(distance(i,j))
				report.write(str(distance(i,j))+" ")
			#matrix.append([])
			report.write("\n")
			#row+=1
		report.close()
		subprocess.call(["java", "-Xms1g", "-Xmx40g", "-jar", "scripts"+os.sep+"Hungarian.jar", "preprocessing"+os.sep+"matrix.txt", reportfile])

	prec(automaton, alph, positive, length, K, reportfile)	

if __name__ == "__main__":
	
	i = sys.argv[1:]
	automaton = i[0]
	positive = i[1]
	alphabet = i[2]
	typ = i[3]
	parameterk = i[4]
	if typ == "MDL" or typ == "RPNI" or typ== "EDSM" or typ == "LSTAR":
		aut = automaton[automaton.rfind(os.sep)+1:]

		reportfile = "result"+os.sep+"precision_report_"+aut+"_with_Hungarian_Algorithm.txt"
		report = open(reportfile,"w")
		report.write("Precision report using "+typ+" algorithm for the discovery task\n")
		report.close()
		for i in range(2, int(parameterk)+1):
			length = i+1
			K = i
			precisionHung(automaton, positive, alphabet, length, K, reportfile)
		
		print("\nPrecision report written in the result folder")

	elif typ == "DECLAREMINER":
		aut = automaton[automaton.rfind(os.sep)+1:]

		reportfile = "result"+os.sep+"precision_report_"+aut+"_with_Hungarian_Algorithm.txt"
		report = open(reportfile,"w")
		report.write("Precision report using "+typ+" algorithm for the discovery task\n")
		report.close()
		for i in range(2, int(parameterk)+1):
			length = i+1
			K = i
			precisionDOT(automaton, alphabet, positive, length, K, reportfile)

		print("\nPrecision report written in the result folder")


