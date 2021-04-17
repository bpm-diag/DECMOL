import os, sys, random

def build_sets(positive, negative, reportfile, num):
	report = open("generalization"+os.sep+reportfile,"a")
	report.write("Generalization \n")
	
	logp = open(positive,"r")
	logn = open(negative,"r")

	kp = []
	for line in logp:
		kp.append(line)

	kn = []
	for line in logn:
		kn.append(line)

	k = num
	dimp = len(kp)//k
	dimn = len(kn)//k

	yp = 0
	yn = 0
	for i in range(k):

		if not os.path.exists("generalization"+os.sep+str(i)):
			os.mkdir("generalization"+os.sep+str(i))

		pos = (dimp*70)//100
		neg3 = (dimn*30)//100
		neg2 = (dimn*20)//100
		neg1 = (dimn*10)//100


		randp = random.sample(range(yp,yp+dimp),pos)
		randn = random.sample(range(yn,yn+dimn),neg3)

		fp = open("generalization"+os.sep+str(i)+os.sep+"positive.txt", "w")
		fn1 = open("generalization"+os.sep+str(i)+os.sep+"negative1.txt","w")
		fn2 = open("generalization"+os.sep+str(i)+os.sep+"negative2.txt","w")
		fn3 = open("generalization"+os.sep+str(i)+os.sep+"negative3.txt","w")
	

		for j in range(pos):
			fp.write(kp[randp[j]])

		for j in range(neg1):
			fn1.write(kn[randn[j]])

		for j in range(neg2):
			fn2.write(kn[randn[j]])

		for j in range(neg3):
			fn3.write(kn[randn[j]])

		report.write("Generalization k "+str(i)+"\n")
		report.write("Number of examples: "+str(dimp+dimn)+"\n")
		report.write("Number of positive examples: "+str(pos)+"\n")
		report.write("Number of negative examples: 10% "+str(neg1)+"\n")
		report.write("Number of negative examples: 20% "+str(neg2)+"\n")
		report.write("Number of negative examples: 30% "+str(neg3)+"\n\n")
		fn3.close()
		fn2.close()
		fn1.close()

		yn += dimn
		yp += dimp

	report.close()
		
	
if __name__ == "__main__":
	#creation of k different sub-logs for model learning. 
	file = sys.argv[1:]
	positive = file[0]
	negative = file[1]
	K = file[2]
	reportfile = "report_sublog.txt"
	if not os.path.exists("generalization"):
		os.mkdir("generalization")  
	
	report = open("generalization"+os.sep+reportfile,"w")
	report.close()
	build_sets(positive, negative ,reportfile, int(K))

	