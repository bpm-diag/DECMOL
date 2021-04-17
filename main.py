import sys, subprocess, getopt, os

#subprocess.call(" python script2.py 1", shell=True)
#subprocess.call(['java', '-jar', 'rum-0.5.12.jar'])

def help():
    print("-e <eventlog> Pre-processing")
    print("-a <RPNI | EDSM | MDL | LSTAR> <alphabet.txt> <positive.txt> <negative.txt> Building automaton with model learning algorithms")
    print("-p <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <automaton.txt | automaton.dot> <positive.txt> <alphabet.txt> <K> Calculation precision")
    print("-g <positive.txt> <negative.txt> <N> Generalization")
    print("-h help")

def options(argv):
    if(len(argv) == 0):
        help()
        sys.exit(0)

    elif(argv[0] == '-e' and (len(argv) < 2 or len(argv) > 2)):
        print("Error")
        help()
        sys.exit(2)

    elif(argv[0] == '-p' and (len(argv) < 6 or len(argv) > 6)):
        print("Error")
        help()
        sys.exit(2)

    elif(argv[0] == '-g' and (len(argv) < 2 or len(argv) > 4 or len(argv) == 3)):
        print("Error")
        help()
        sys.exit(2)

    elif(argv[0] == '-a'):
        if(argv[1] == "RPNI" or argv[1] == "EDSM"):
            if(len(argv) < 5 or len(argv) > 5):
                if(len(argv) > 5):
                    print("Error! Too many arguments")
                else:
                    print("Error! Some input is missing")
                help()
                sys.exit(2)
        elif(argv[1] == "MDL"):
            if(len(argv) < 4 or len(argv) > 4):
                print("Error! MDL takes only positive examples")
                help()
                sys.exit(2)

    if(argv[0] == '-h'):
        help()
        sys.exit()

    elif(argv[0] == '-e'):
        #launch python script for preprocessing
        event = argv[1]
        subprocess.call(["python3","scripts"+os.sep+"DataProcessing.py", event])
        
    elif(argv[0] == '-a'):
        #run java.jar for automaton creation
        algorithm = argv[1]
        alphabet = argv[2]
        positive = argv[3]
        negative = ""
        if(len(argv) == 5):
            negative = argv[4]
        subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", algorithm, alphabet, positive, negative])

    elif(argv[0] == '-p'):
        #run precision.py
        typ = argv[1]
        automaton = argv[2]
        positive = argv[3]
        alphabet = argv[4]
        k = argv[5]
        subprocess.call(["python3","scripts"+os.sep+"Precision.py", automaton, positive, alphabet, typ, k])

    elif(argv[0] == '-g'):
        if(len(argv)==2):
            k = argv[1]
            subprocess.call(["python3","scripts"+os.sep+"GeneralizationML.py","preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"negative3.txt", k])
        else:
            positive = argv[1]
            negative = argv[2]
            k = argv[3]
            subprocess.call(["python3","scripts"+os.sep+"GeneralizationML.py", positive, negative, k])
        for i in range(0,int(k)):
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "MDL", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt",""])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "RPNI", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "RPNI", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "RPNI", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "EDSM", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "EDSM", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "EDSM", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "LSTAR", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "LSTAR", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", "LSTAR", "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
        subprocess.call(["python3","scripts"+os.sep+"Minimize.py", k])
        
    else:
        print("Invalid Option")
        help()
        sys.exit(2)

if __name__ == "__main__":
    options(sys.argv[1:])
