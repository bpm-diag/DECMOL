import pm4py
from pm4py.algo.filtering.log.attributes import attributes_filter
import random
import os, sys, shutil

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
	
def compute(log, reportfile):
	fp = open("preprocessing"+os.sep+"positive.txt", "w")

	report = open(reportfile,"a")

	k = 0
	for i in log:
		s = buildString(i)
		if k == len(log)-1:
			fp.write(s)
		else:
			fp.write(s+"\n")
		k+=1

	fp.close()
	report.write("Number of examples: "+str(len(log))+"\n")
	report.close()
	
def buildString(trace):
	s = ""
	for i in trace:
		i = (i['concept:name']).lower().replace(" ","").replace("\\\\","-")
		s+=i+" "
	#print(s)
	return s

def build_set(file, reportfile):
	report = open(reportfile,"a")
	report.write("File: "+file+"\n")
	report.close()

	log = pm4py.read_xes(file)
	getAlphabet(log, reportfile)
	compute(log, reportfile)
	
	
if __name__ == "__main__":
	file = sys.argv[1:]
	if not os.path.exists("result"):
		os.mkdir("result")
	elif os.path.exists("result"):
		pathname = os.path.dirname(sys.argv[0])
		shutil.rmtree("result")
		os.mkdir("result")
	if not os.path.exists("preprocessing"):
		os.mkdir("preprocessing") 
	elif os.path.exists("preprocessing"):
		pathname = os.path.dirname(sys.argv[0])
		shutil.rmtree("preprocessing")
		os.mkdir("preprocessing")
		
	reportfile = "result"+os.sep+"report_log.txt"
	report = open(reportfile,"w")
	report.close()

	build_set(file[0],reportfile)
