import sys, os
if __name__ == "__main__":
	#creation of k different sub-logs for model learning. 
	file = sys.argv[1:]
	alg = file[0]
	k = file[1]
	#we can not use set because in Model Learning is relevant the order of alphabet.
	s = dict()
	if alg == "MDL":
		for i in range(int(k)):
			path = "generalization"+os.sep+str(i)
			f = open(path+os.sep+"positive.txt","r")
			for j in f:
				j = j.strip()
				j = j.split(" ")
				for k in j:
					s[k]=""
			f.close()
			fa = open(path+os.sep+"alphabet.txt","w")
			for i in s:
				fa.write(i+"\n")
			fa.close()
	else:
		for i in range(int(k)):
			path = "generalization"+os.sep+str(i)
			f = open(path+os.sep+"positive.txt","r")
			for j in f:
				j = j.strip()
				j = j.split(" ")
				for k in j:
					s[k]=""
			f.close()
			f = open(path+os.sep+"negative1.txt","r")
			for j in f:
				j = j.strip()
				j = j.split(" ")
				for k in j:
					s[k]=""
			f.close()
			f = open(path+os.sep+"negative2.txt","r")
			for j in f:
				j = j.strip()
				j = j.split(" ")
				for k in j:
					s[k]=""
			f.close()
			f = open(path+os.sep+"negative3.txt","r")
			for j in f:
				j = j.strip()
				j = j.split(" ")
				for k in j:
					s[k]=""
			f.close()
			fa = open(path+os.sep+"alphabet.txt","w")
			for i in s:
				fa.write(i+"\n")
			fa.close()


