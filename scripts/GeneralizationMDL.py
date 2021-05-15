import os, sys, shutil 


def build_sets(positive,reportfile, num):

	report = open("generalization"+os.sep+reportfile,"a")
	report.write("Generalization \n")

	log = open(positive,"r")

	dim = len(log.readlines())//num
	log.close()
	log = open(positive,"r")
	y = 0
	c = 0
	for i in range(num):
		os.mkdir("generalization"+os.sep+str(i))

	fp = open("generalization"+os.sep+str(y)+os.sep+"positive.txt", "w")	
	report.write("Generalization k "+str(y)+"\n")
	for i in log:
		fp.write(i)
		c+=1
		if c == dim:
			y = y+1
			if y < num:
				report.write("Number of examples: "+str(c)+"\n\n")
				c = 0
				report.write("Generalization k "+str(y)+"\n")
				fp.close()
				fp = open("generalization"+os.sep+str(y)+os.sep+"positive.txt", "w")
	
	report.write("Number of examples: "+str(c)+"\n\n")
	fp.close()	
	report.close()

if __name__ == "__main__":
	#creation of k different sub-logs for model learning. 
	file = sys.argv[1:]
	positive = file[0]
	K = file[1]
	reportfile = "report_log.txt"
	if not os.path.exists("generalization"):
		os.mkdir("generalization")
	elif os.path.exists("generalization"):
		pathname = os.path.dirname(sys.argv[0])
		shutil.rmtree("generalization")
		os.mkdir("generalization")
	
	report = open("generalization"+os.sep+reportfile,"w")
	report.close()
	build_sets(positive,reportfile, int(K))

	