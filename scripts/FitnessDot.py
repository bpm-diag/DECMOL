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

def fitnessHung(automaton, positive, length, K, reportfile, numfolder, mapping):
	def fitness(automaton, positive, length, K, reportfile, numfolder, mapping):
		reportf = open(reportfile,"a")
		if not os.path.exists("preprocessing"):
			os.mkdir("preprocessing")  
		report = open("preprocessing"+os.sep+"matrix.txt","w")
		reportf.write("Fitness automaton "+str(numfolder)+" taking into account behaviours of length = "+str(K)+"\n")
		

		reportf.close()
		
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
		
		fp.close()
		paths = []
		pathset = set()
		for a in transition_function:
			myDFS(transition_function,a,length,paths,pathset)



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

	fitness(automaton, positive, length, K, reportfile, numfolder, mapping)

def generalization(reportfile, n):
	ar = []
	n = n-1
	j = 0
	
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

if __name__ == "__main__":
	
	inp = sys.argv[1:]
	positive = inp[0]
	parameterk = int(inp[1])
	n = int(inp[2])
	automaton = inp[3]
	y = inp[4]
	alphabet = set()
		
	f = open(positive,"r")
	for j in f:
		j = j.strip()
		j = j.split(" ")
		for k in j:
			alphabet.add(k)
	f.close()
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

	
	reportfile = "result"+os.sep+"generalization_report_DOT_files.txt"
		
	for j in range(2, n+1):
		length = j+1
		K = j
		fitnessHung(automaton, positive, length, K, reportfile, y , mapping)

	if inp[5] == "1":
		generalization(reportfile, n)
		print("\nGeneralization report written in the result folder")



