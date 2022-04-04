import pm4py

def read_log(log_file):
    def processed(text):
        #make the name match the ones used by DECMOL
        return '"'+text.replace(" ", "").lower()+'"'
    #input: xes file. output: list of lists
    log = pm4py.read_xes(log_file)
    traces = []
    for trace_log in log:
        trace = []
        for event in trace_log:
            trace.append(processed(event['concept:name']))
        traces.append(trace)
    return traces 
    
import random

def create_sublogs(log,h): #crea h coppie (log_train,log_test), con log_train+log_test = log e log_train h-1 volte log_test e non-overlapping log_tests
    trains = []
    tests = []
    random.shuffle(log)
    log_len = len(log)
    for j in range(h):
        tests.append([])
    j=0
    for i in range(log_len):
        tests[j].append(log[i])
        j = (j+1) % h
    for j in range(h):
        train = []
        for trace in log:
            if trace not in tests[j]:
                train.append(trace)
        trains.append(train)
    return trains,tests
    
def log2txt(log,name):
    with open(sublog_dir+os.sep+name,'w') as f:
        for trace in log:
            for event in trace:
                f.write(event[1:-1]) #toglie le virgolette
                f.write(' ')
            f.write('\n')

import pydot
import pythomata

def dot2dfa(dot_file):
    digraph = pydot.graph_from_dot_file(dot_file)[0]
    states = set()
    accepting_states = set()

    nodes = digraph.get_nodes()
    for node in nodes:
        state = node.get_name()
        if state != '__start0':
            states.add(state)
        if node.get_attributes()['shape']== '"doublecircle"':
            accepting_states.add(state)
    transition_function = dict()
    for state in states:
        transition_function[state]=dict()
    alphabet = set()
    edges = digraph.get_edges()
    for edge in edges:
        source = edge.get_source()
        label = edge.get_label()
        destination = edge.get_destination()
        if source != '__start0':
            transition_function[source][label]=destination
            alphabet.add(label)
        else:
            initial_state = destination
    dfa = pythomata.SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    return dfa.trim()
    
import os

def create_dir(dir_name):
    isExist = os.path.exists(dir_name)
    if not isExist:
        os.mkdir(dir_name)
        
import subprocess
import shutil

def remove_dir(dir_name):
    isExist = os.path.exists(dir_name)
    if isExist:
        shutil.rmtree(dir_name)
        
def log_name(posORneg,trainORtest,i):
        return str(h)+'_'+posORneg+'_'+trainORtest+'_'+str(i)
    
def list_of_lists2xes(log,name):
    out = open(name,'w')
    out.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    out.write('<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">\n')
    for i in range(len(log)):
        trace = log[i]
        out.write('\t<trace>\n')
        out.write('\t\t<string key="concept:name" value="Case No. {}"/>\n'.format(i))
        for event in trace:
            out.write('\t\t<event>\n')
            out.write('\t\t\t<string key="concept:name" value="{}"/>\n'.format(event[1:-1])) #gli indici rimuovono gli apici
            out.write('\t\t</event>\n') 
        out.write('\t</trace>\n')
    out.write('</log>\n')
    out.close()


import subprocess
import shutil

def remove_dir(dir_name):
    isExist = os.path.exists(dir_name)
    if isExist:
        shutil.rmtree(dir_name)
        
def log_name(posORneg,trainORtest,i):
        return str(h)+'_'+posORneg+'_'+trainORtest+'_'+str(i)
    
def list_of_lists2xes(log,name):
    out = open(name,'w')
    out.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    out.write('<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">\n')
    for i in range(len(log)):
        trace = log[i]
        out.write('\t<trace>\n')
        out.write('\t\t<string key="concept:name" value="Case No. {}"/>\n'.format(i))
        for event in trace:
            out.write('\t\t<event>\n')
            out.write('\t\t\t<string key="concept:name" value="{}"/>\n'.format(event[1:-1])) #gli indici rimuovono gli apici
            out.write('\t\t</event>\n') 
        out.write('\t</trace>\n')
    out.write('</log>\n')
    out.close()


def generalization(algorithm,pos_log_file,neg_log_file,alphabet,k,h):
    pos_log = read_log(pos_log_file)
    neg_log = read_log(neg_log_file)
    print()
    pos_trains,pos_tests = create_sublogs(pos_log,h)
    neg_trains,neg_tests = create_sublogs(neg_log,h)
    global sublog_dir
    sublog_dir = 'sublogs'
    create_dir(sublog_dir)

    remove_dir(algorithm)
    pos_generalization = 0
    neg_generalization = 0
    for i in range(h):
        #train
        pos_train_log = pos_trains[i] 
        pos_train_name = log_name('pos','train',i)
        log2txt(pos_train_log,pos_train_name)
        positive = sublog_dir+os.sep+pos_train_name
        neg_train_log = neg_trains[i]
        neg_train_name = log_name('neg','train',i)
        log2txt(neg_train_log,neg_train_name)
        negative = sublog_dir+os.sep+neg_train_name
        subprocess.call(["java", "-Xms1g", "-Xmx40g","-jar", "ModelLearning.jar", algorithm, alphabet, positive, negative])
        #read automaton
        files = os.listdir(algorithm)
        for file in files:
            if 'automaton' in file:
                automaton_file = algorithm+os.sep+file
        #test
        pos_test_log = pos_tests[i]
        pos_test_name = sublog_dir+os.sep+log_name('pos','test',i)+'.xes'
        list_of_lists2xes(pos_test_log,pos_test_name) 
        pos_result = subprocess.run(['python', 'recall.py', pos_test_name, automaton_file, str(k)], stdout=subprocess.PIPE)
        curr_pos_gen = float(pos_result.stdout.decode('utf-8').strip())
        print('fitness: ',curr_pos_gen)
        pos_generalization += curr_pos_gen
        neg_test_log = neg_tests[i]
        neg_test_name = sublog_dir+os.sep+log_name('neg','test',i)+'.xes'
        list_of_lists2xes(neg_test_log,neg_test_name)
        neg_result = subprocess.run(['python', 'neg_recall.py', neg_test_name, automaton_file, alphabet, str(k)], stdout=subprocess.PIPE)
        curr_neg_gen = float(neg_result.stdout.decode('utf-8').strip())
        print('fitness: ',curr_neg_gen)
        neg_generalization += curr_neg_gen
        shutil.rmtree(algorithm)
        print()

    pos_generalization = pos_generalization/h  #ToDo (optional): weight generalization with number elements to handle the fact that last sublog may have less traces
    neg_generalization = neg_generalization/h

    print(pos_generalization)
    print(len(pos_log))
    print(neg_generalization)
    print(len(neg_log))


import sys

if __name__ == "__main__":
    algorithm = sys.argv[1]
    pos_log_file = sys.argv[2] #xes
    neg_log_file = sys.argv[3] #xes
    alphabet = sys.argv[4] #txt
    k = int(sys.argv[5]) #fitness parameter
    h = int(sys.argv[6]) #number sublogs
    generalization(algorithm,pos_log_file,neg_log_file,alphabet,k,h)
    
