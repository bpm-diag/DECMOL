from pythomata import SimpleDFA
from graphviz import Digraph
from itertools import combinations
from Levenshtein import *
import sys, subprocess, os, getopt

def myDFS(trans_dict,start,length,paths,pathset,path=[],st=""): 
	    path=path+[start] 
	    if len(path)==length:
	    	pathset.add(st)
	    	paths.append(path)

	    else:
	    	if not start in trans_dict:
	    		return
	    	for node in trans_dict[start]:
	    		st+=node[1]+" "
	    		myDFS(trans_dict,node[0],length,paths,pathset,path,st)
	    		st=st[:-len(node[1])-1]

def fitnessHung(automaton, positive, alphabet, length, K, reportfile, numfolder, numaut):
	def fitness(automaton, positive, alph, length, K, reportfile, numfolder, numaut):
		reportf = open(reportfile,"a")
		if not os.path.exists("preprocessing"):
			os.mkdir("preprocessing")  
		report = open("preprocessing"+os.sep+"matrix.txt","w")
		if numaut == 0:
			reportf.write("Fitness automaton in folder "+str(numfolder)+" taking into account behaviours of length = "+str(K)+"\n")
		else:
			reportf.write("Fitness automaton"+str(numaut)+" in folder "+str(numfolder)+" taking into account behaviours of length = "+str(K)+"\n")

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
				x+=1
				'''
				if(x==123):
					x=65
				'''
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
		
		#transformation into automaton for DFS
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

		#behaviours inside the log
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
						sum += line[j]+ " "
					logset.add(sum)
		fp.close()

		report.write(str(len(logset))+"\n")
		report.write(str(len(pathset))+"\n")
		
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
		for j in abclog:
			for i in abcautomaton:
				#matrix[row].append(distance(i,j))
				report.write(str(distance(j,i))+" ")
			#matrix.append([])
			report.write("\n")
			#row+=1
		report.close()
		subprocess.call(["java", "-Xms1g", "-Xmx40g", "-jar", "scripts"+os.sep+"Hungarian.jar", "preprocessing"+os.sep+"matrix.txt", reportfile])

	fitness(automaton, positive, alphabet, length, K, reportfile, numfolder, numaut)

def generalization(reportfile, alg, n):
	ar = []
	n = n-1
	j = 0
	
	if alg == "MDL":
		f = open(reportfile, "r")
		for i in f:
			if len(i) > 1: 
				i = i.strip()
				if i[2:].isnumeric():
					ar.insert(j, float(i))
					j+=1
		dim = len(ar)//n
		f.close()
		f = open(reportfile,"a+")
		for x in range(n):
			count = 0.0
			j=2
			z=0
			for y in range(dim):
				count+=ar[x+z]
				z+=n
			f.write("Generalization for behaviours of length = "+str(j+x)+" is : "+str(count/dim)+"\n")
	else:
		f = open(reportfile, "r")
		for i in f:
			if len(i) > 1: 
				i = i.strip()
				if i[2:].isnumeric():
					ar.insert(j, float(i))
					j+=1
		dim = len(ar)//n
		f.close()
		f = open(reportfile,"a+")
		j=1
		for x in range(dim):
			count = 0.0
			z=0
			for y in range(n):
				count+=ar[x+z]
				z+=(n*n)
			j+=1
			f.write("Generalization for automaton "+str((x//n)+1)+" with behaviours length = "+str(j)+" is : "+str(count/n)+"\n")
			if j==n+1: 
				j=1

if __name__ == "__main__":
	
	inp = sys.argv[1:]
	positive = inp[0]
	alphabet = inp[1]
	typ = inp[2]
	parameterk = int(inp[3])
	n = int(inp[4])
	folder = "generalization"+os.sep
	if typ == "MDL" or typ == "RPNI" or typ== "EDSM" or typ == "LSTAR":
	
		reportfile = "result"+os.sep+"generalization_report_with_Hungarian_Algorithm.txt"
		report = open(reportfile,"w")
		report.write("Generalization report using "+typ+" algorithm for the discovery task\n")
		report.close()
		if typ == "MDL":
			for i in range(parameterk):
				automaton = "generalization"+os.sep+str(i)+os.sep+"MDL"+os.sep+"automaton.txt"
				for j in range(2, n+1):
					length = j+1
					K = j
					if len(inp)==6:
						fitnessHung(automaton, positive, alphabet+str(i)+os.sep+"alphabet.txt", length, K, reportfile, i, 0)
					else:
						fitnessHung(automaton, positive, alphabet, length, K, reportfile, i, 0)
			generalization(reportfile,typ,n)
		else:
			for i in range(parameterk):
				for j in range(1, 4):
					automaton = "generalization"+os.sep+str(i)+os.sep+typ+os.sep+"automaton"+str(j)+".txt"
					for z in range(2, n+1):
						length = z+1
						K = z
						if len(inp)==6:
							fitnessHung(automaton, positive, alphabet+str(i)+os.sep+"alphabet.txt", length, K, reportfile, i ,j)
						else:
							fitnessHung(automaton, positive, alphabet, length, K, reportfile, i ,j)
			generalization(reportfile,typ,n)

		print("\nGeneralization report written in the result folder")


