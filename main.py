import sys, subprocess, getopt, os, glob, shutil

#subprocess.call(" python script2.py 1", shell=True)
#subprocess.call(['java', '-jar', 'rum-0.5.12.jar'])

def help():
    print("-e <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <EventLog> Pre-processing")
    print("-a <RPNI | EDSM | MDL | LSTAR> <alphabet.txt> <positive.txt> <negative.txt> Building automaton with model learning algorithms")
    print("-p <RPNI | EDSM | MDL | LSTAR | DeclareMiner> <automaton.txt | automaton.dot> <positive.txt> <alphabet.txt> <K> Calculation precision")
    print("-g <RPNI | EDSM | MDL | LSTAR> <positive.txt> <negative.txt> <N> <K> Computing generalization with respect to Model Learning algorithms")
    print("-d <positive.txt> <N> <K> <automaton1.dot> ... <automatonN> Generalization with respect to DeclareMiner algorithm")
    print("-c <RPNI | EDSM | MDL | LSTAR> <K1> <N> <K2> <EventLog> All automated functionality")
    print("-h help")

def options(argv):
    if len(argv) == 0:
        help()
        sys.exit(0)

    elif argv[0].lower() == '-c' and len(argv) != 6:
        print("Error, wrong number (or type) of arguments")
        help()
        sys.exit(2)

    elif argv[0].lower() == '-e' and (len(argv) < 3 or len(argv) > 3):
        print("Error, wrong number (or type) of arguments")
        help()
        sys.exit(2)

    elif argv[0].lower() == '-p' and (len(argv) < 6 or len(argv) > 6):
        print("Error, wrong number (or type) of arguments")
        help()
        sys.exit(2)

    elif argv[0].lower() == '-g' and (len(argv) == 1 or (argv[1].upper()!="MDL" and len(argv) == 5) or (argv[1].upper()=="MDL" and len(argv) < 4) or 
        (argv[1].upper()=="MDL" and len(argv) > 5) or (argv[1].upper()!="MDL" and len(argv) < 3) or (argv[1].upper()!="MDL" and len(argv) > 6)):
        print("Error, wrong number (or type) of arguments")
        help()
        sys.exit(2)

    elif argv[0].lower() == '-d' and (len(argv) < 7):
        print("Error! Some input is missing. Take into account that is needed at least two automata for executing this functionality")
        sys.exit(2)

    elif argv[0].lower() == '-a':
        if argv[1].upper() == "RPNI" or argv[1].upper() == "EDSM":
            if len(argv) < 5 or len(argv) > 5:
                if len(argv) > 5:
                    print("Error! Too many arguments")
                else:
                    print("Error! Some input is missing")
                help()
                sys.exit(2)
        elif argv[1].upper() == "MDL":
            if len(argv) < 4 or len(argv) > 4:
                print("Error! MDL takes only positive examples")
                help()
                sys.exit(2)

    if argv[0].lower() == '-h':
        help()
        sys.exit()

    elif argv[0].lower() == '-e':
        #launch python script for preprocessing
        event = argv[2]
        algorithm = (argv[1]).upper()
        if algorithm == "MDL" or algorithm == "DECLAREMINER":
            subprocess.call(["python3","scripts"+os.sep+"DataProcessingMDL.py", event])
        else:
            subprocess.call(["python3","scripts"+os.sep+"DataProcessing.py", event])
        
    elif argv[0].lower() == '-a':
        #run java.jar for automaton creation
        algorithm = (argv[1]).upper()
        alphabet = argv[2]
        positive = argv[3]
        negative = ""
        if len(argv) == 5:
            negative = argv[4]
        subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", algorithm, alphabet, positive, negative])

    elif argv[0].lower() == '-p':
        #run precision.py
        typ = (argv[1]).upper()
        automaton = argv[2]
        positive = argv[3]
        alphabet = argv[4]
        k = argv[5]
        if not os.path.exists("result"):
            os.mkdir("result")  
        subprocess.call(["python3","scripts"+os.sep+"Precision.py", automaton, positive, alphabet, typ, k])
        subprocess.call(["python3","scripts"+os.sep+"PrecisionHungarian.py", automaton, positive, alphabet, typ, k])

    elif argv[0].lower() == '-g':
        alg = (argv[1]).upper()
        if alg == "RPNI" or alg == "EDSM" or alg == "LSTAR":
            if len(argv)==4:
                if not os.path.exists("preprocessing"):
                    print("Error, no files available in pre-processing folder (hint run -e)")
                    sys.exit(2)
                elif os.path.exists("preprocessing"):
                    path, dirs, files = next(os.walk("preprocessing"))
                    file_count = len(files) 
                    if file_count < 5:
                        print("Error, the files available in pre-processing are not enough (hint run -e)")
                        sys.exit(2)
                k = argv[2]
                behaviors = argv[3]
                subprocess.call(["python3","scripts"+os.sep+"GeneralizationML.py","preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"negative3.txt", k])
                subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",k, os.path.abspath(__file__)[:-8]])
                for i in range(0,int(k)):
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
                #subprocess.call(["python3","scripts"+os.sep+"Minimize.py", k, alg, "preprocessing"+os.sep+"alphabet.txt"])
                subprocess.call(["python3","scripts"+os.sep+"Fitness.py", "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", alg, k, behaviors])

            else:
                positive = argv[2]
                negative = argv[3]
                k = argv[4]
                behaviors = argv[5]

                subprocess.call(["python3","scripts"+os.sep+"GeneralizationML.py", positive, negative, k])
                #compute alphabet.txt
                subprocess.call(["python3","scripts"+os.sep+"ComputeAlphabet.py", alg, k])
                subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",k, os.path.abspath(__file__)[:-8]])

                for i in range(0,int(k)):
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
                #subprocess.call(["python3","scripts"+os.sep+"Minimize.py", k, alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt"])
                subprocess.call(["python3","scripts"+os.sep+"Fitness.py", positive, "generalization"+os.sep, alg, k, behaviors,"False"])

        elif alg == "MDL":
            if len(argv)==4:
                if not os.path.exists("preprocessing"):
                    print("Error, no files available in pre-processing folder (hint run -e)")
                    sys.exit(2)
                k = argv[2]
                behaviors = argv[3]
                subprocess.call(["python3","scripts"+os.sep+"GeneralizationMDL.py","preprocessing"+os.sep+"positive.txt", k])
                subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",k, os.path.abspath(__file__)[:-8]])

                for i in range(0,int(k)):
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt",""])
                #subprocess.call(["python3","scripts"+os.sep+"Minimize.py", k, alg, "preprocessing"+os.sep+"alphabet.txt"])
                subprocess.call(["python3","scripts"+os.sep+"Fitness.py", "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", "MDL", k, behaviors])
                
            else:
                positive = argv[2]
                k = argv[3]
                behaviors = argv[4]
                subprocess.call(["python3","scripts"+os.sep+"GeneralizationMDL.py", positive, k, alg])
                subprocess.call(["python3","scripts"+os.sep+"ComputeAlphabet.py", alg, k])
                subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",k, os.path.abspath(__file__)[:-8]])

                for i in range(0,int(k)):
                    subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt",""])
                #subprocess.call(["python3","scripts"+os.sep+"Minimize.py", k, alg, "generalization"+os.sep+str(i)+os.sep+"alphabet.txt"])
                subprocess.call(["python3","scripts"+os.sep+"Fitness.py", positive, "generalization"+os.sep, "MDL", k, behaviors,"False"])

    elif argv[0].lower() == '-d':
        positive = argv[1]
        n = argv[2]
        k = argv[3]
        if int(n)+4 != len(argv):
            print("Error, some input is missing")
            sys.exit(2)
        else:
            if not os.path.exists("result"):
                os.mkdir("result")  
            reportfile = "result"+os.sep+"generalization_report_DOT_files.txt"
            report = open(reportfile, "w")
            report.write("Generalization report using DeclareMiner algorithm for the discovery task\n")
            report.close()

            x = 4
            for i in range(int(n)):
                if i == int(n)-1:
                    subprocess.call(["python3","scripts"+os.sep+"FitnessDot.py", positive, n, k, argv[x+i], str(i+1), "1"])
                else:
                    subprocess.call(["python3","scripts"+os.sep+"FitnessDot.py", positive, n, k, argv[x+i], str(i+1), "0"])

    elif argv[0].lower() == '-c':
        alg = argv[1].upper()
        k1 = argv[2]
        n = argv[3]
        k2 = argv[4]
        event = argv[5]

        files = []
        path = os.path.abspath(__file__)[:-8]+os.sep+alg
        

        if alg == "MDL":

            if os.path.exists("MDL"):
                pathname = os.path.dirname(sys.argv[0])
                shutil.rmtree("MDL")
                
            subprocess.call(["python3","scripts"+os.sep+"DataProcessingMDL.py", event])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "preprocessing"+os.sep+"positive.txt", ""])
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path,i)) and 'automaton' in i:
                    files.append(i)
            subprocess.call(["python3","scripts"+os.sep+"Precision.py", "MDL"+os.sep+files[0], "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", "MDL", k1])
            subprocess.call(["python3","scripts"+os.sep+"PrecisionHungarian.py", "MDL"+os.sep+files[0], "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", "MDL", k1])            
            subprocess.call(["python3","scripts"+os.sep+"GeneralizationMDL.py","preprocessing"+os.sep+"positive.txt", n])
            subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",n, os.path.abspath(__file__)[:-8]])
            
            for i in range(int(n)):
                subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt",""])
                
            subprocess.call(["python3","scripts"+os.sep+"Fitness.py", "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", "MDL", n, k2])

        else:
            if os.path.exists(alg):
                pathname = os.path.dirname(sys.argv[0])
                shutil.rmtree(alg)

            subprocess.call(["python3","scripts"+os.sep+"DataProcessing.py", event])
            subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"negative3.txt"])
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path,i)) and 'automaton' in i:
                    files.append(i)
            subprocess.call(["python3","scripts"+os.sep+"Precision.py", alg+os.sep+files[0], "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", alg, k1])
            subprocess.call(["python3","scripts"+os.sep+"PrecisionHungarian.py", alg+os.sep+files[0], "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", alg, k1])            
            subprocess.call(["python3","scripts"+os.sep+"GeneralizationML.py","preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"negative3.txt", n])
            subprocess.call(["python3","scripts"+os.sep+"xes-master"+os.sep+"Buildxes.py",n, os.path.abspath(__file__)[:-8]])

            for i in range(int(n)):
                subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative1.txt"])
                subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative2.txt"])
                subprocess.call(["java", "-jar", "scripts"+os.sep+"ModelLearning.jar", alg, "preprocessing"+os.sep+"alphabet.txt", "generalization"+os.sep+str(i)+os.sep+"positive.txt","generalization"+os.sep+str(i)+os.sep+"negative3.txt"])
            subprocess.call(["python3","scripts"+os.sep+"Fitness.py", "preprocessing"+os.sep+"positive.txt", "preprocessing"+os.sep+"alphabet.txt", alg, n, k2])


    else:   
        print("Invalid Option")
        help()
        sys.exit(2)

if __name__ == "__main__":
    options(sys.argv[1:])
