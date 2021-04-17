import pm4py
from pm4py.algo.filtering.log.attributes import attributes_filter
import random
import os, sys

def getAlphabet(log, reportfile): 
	c = 0 
	activities = attributes_filter.get_attribute_values(log, "concept:name")

	f = open("preprocessing"+os.sep+"alphabet.txt", "w")
	report = open(reportfile,"a")

	for i in activities:
		i = i.lower()
		i = i.replace(" ","")
		i = i.replace("\\\\","-")
		if not c == len(activities)-1:
			f.write(i+"\n")
		else:
			f.write(i)
		c+=1

	f.close()
	report.write("Alphabet size "+str(len(activities))+"\n")
	report.close()
	return
	
def computeRandom(log,reportfile):
	fp = open("preprocessing"+os.sep+"positive.txt", "w")
	fn1 = open("preprocessing"+os.sep+"negative1.txt","w")
	fn2 = open("preprocessing"+os.sep+"negative2.txt","w")
	fn3 = open("preprocessing"+os.sep+"negative3.txt","w")

	report = open(reportfile,"a")

	unique = set()
	for i in log:
		s = buildString(i)
		unique.add(s)
	l = len(unique)
	uniquev = list(unique)
	rand = random.sample(range(0,l),l)
	pos = (l*70)//100
	neg3 = (l*30)//100
	neg2 = (l*20)//100
	neg1 = (l*10)//100
		
	for i in range(0,pos):
		x = rand[i]
		fp.write(uniquev[x]+"\n")
	for i in range(pos, pos+neg1):
		x = rand[i]
		fn1.write(uniquev[x]+"\n")
	for i in range(pos, pos+neg2):
		x = rand[i]
		fn2.write(uniquev[x]+"\n")
	for i in range(pos, pos+neg3):
		x = rand[i]
		fn3.write(uniquev[x]+"\n")

	report.write("Number of examples: "+str(l)+"\n")
	report.write("Number of positive examples: "+str(pos)+"\n")
	report.write("Number of negative examples: 10% "+str(neg1)+"\n")
	report.write("Number of negative examples: 20% "+str(neg2)+"\n")
	report.write("Number of negative examples: 30% "+str(neg3)+"\n\n")
	report.close()
	fn3.close()
	fn2.close()
	fn1.close()
	
def buildString(trace):
	s = ""
	for i in trace:
		i = (i['concept:name']).lower().replace(" ","").replace("\\\\","-")
		s+=i+" "
	return s

def build_set(file, reportfile):
	report = open(reportfile,"a")
	report.write("File: "+file+"\n")
	report.close()

	log = pm4py.read_xes(file)
	getAlphabet(log, reportfile)
	computeRandom(log, reportfile)
	
	
if __name__ == "__main__":
	file = sys.argv[1:]
	if not os.path.exists("result"):
		os.mkdir("result")  
	if not os.path.exists("preprocessing"):
		os.mkdir("preprocessing")  
	reportfile = "result"+os.sep+"report_log.txt"
	report = open(reportfile,"w")
	report.close()
	build_set(file[0],reportfile)
