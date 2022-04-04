def read_alphabet(alphabet_file):
    alphabet = set()
    with open(alphabet_file) as f:
        for line in f:
            line = '"'+line.strip()+'"'
            alphabet.add(line)
    return alphabet
    

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
    return dfa
    
def complement(dfa,alphabet):
    ### complete the dfa using the *whole* alphabet (given in input) instead of the automaton alphabet
    states = dfa.states
    initial_state = dfa.initial_state
    accepting_states  = dfa.accepting_states
    transition_function = dfa.transition_function
    dfa = pythomata.SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    dfa = dfa.complete()
    ### swapping accepting and non-accepting
    states = dfa.states 
    transition_function = dfa.transition_function 
    accepting_states = set()
    for state in states:
        if not dfa.is_accepting(state):
            accepting_states.add(state)
    compl_dfa = pythomata.SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    ### trim
    compl_dfa = compl_dfa.trim()
    return compl_dfa
    
def log_abstraction(log,k):
    #log is a list of lists. nodes are tuples of events/characters (or special symbol), edges are pairs of nodes
    l = k+1
    nodes = set()
    edges = set()
    special_state = '-'
    nodes.add(special_state)
    for trace in log:
        len_trace = len(trace)
        if len_trace <=k:
            trace = tuple(trace)
            nodes.add(trace)
            edges.add((special_state,trace))
            edges.add((trace,special_state))
        else:
            last_index = len_trace-l+1
            for i in range(0,last_index):
                subtrace = trace[i:i+l] #computing subtraces of len l
                first = tuple(subtrace[:-1])
                second = tuple(subtrace[1:])
                nodes.add(first)
                nodes.add(second)
                edges.add((first,second))
                if i == 0:
                    edges.add((special_state,first))
                if i == last_index-1:
                    edges.add((second,special_state))
    return nodes, edges
    

def edges_freq(edges,log,k):
    #computes the frequency of edges (used for Fitness)
    freqs = dict()
    for edge in edges: 
        #reobtaing the trace/subtrace corresponding to the edge
        first_node,second_node = edge
        if first_node == '-':
            string = ['-']+list(second_node)
        elif second_node == '-':
            string = list(first_node)+['-']
        else:
            string = list(first_node)+[second_node[-1]]
        #counting the number of times the string appears in the log (no matter if as trace or subtrace)
        c = 0
        str_len = len(string)
        for trace in log:
            trace = ['-']+trace+['-']
            for i in range(0,len(trace)-str_len+1):
                if string == trace[i:i+str_len]:
                    c = c+1
        freqs[edge]=c
    return freqs
    
    
from pythomata import SimpleDFA

def myDFS(dfa, s, k, paths, traces, path, trace = []):
    #Compute traces of len <=k
    for trans in dfa.get_transitions_from(s):
        s,a,new_s = trans
        new_path = path.copy()
        new_trace = trace.copy()
        new_path.append(new_s)
        new_trace.append(a)
        if dfa.is_accepting(new_s):
            paths.append(new_path)
            traces.append(new_trace)
        if len(new_trace)<k:
            myDFS(dfa, new_s, k, paths, traces, new_path, new_trace)

def myDFS2(dfa, s, k, paths, traces, path, trace = []):
    #Compute subtraces of len k+1
    for trans in dfa.get_transitions_from(s):
        s,a,new_s = trans
        new_path = path.copy()
        new_trace = trace.copy()
        new_path.append(new_s)
        new_trace.append(a)
        if len(new_trace)<k+1:
            myDFS2(dfa, new_s, k, paths, traces, new_path, new_trace)
        else:
            paths.append(new_path)
            traces.append(new_trace)


def process_abstraction(dfa,k):
    #dfa is the input process
    states = dfa.states
    transitions = dfa.get_transitions()
    start = dfa.initial_state
    accept = dfa.accepting_states
    ###
    paths = []
    traces = []      
    start = dfa.initial_state
    myDFS(dfa, start, k, paths, traces, [start])
    ###
    subpaths = []
    subtraces = []      
    for state in states:
        myDFS2(dfa, state, k, subpaths, subtraces, [state])
    ###
    nodes = set()
    edges = set()
    special_state = '-'
    nodes.add(special_state)
    for trace in traces:
        trace = tuple(trace)
        nodes.add(trace)
        edges.add((special_state,trace))
        edges.add((trace,special_state))
    for i in range(len(subtraces)):
        subtrace = subtraces[i]
        subpath = subpaths[i] #to know if the trace is a prefix or suffix
        first = tuple(subtrace[:-1])
        second = tuple(subtrace[1:])
        nodes.add(first)
        nodes.add(second)
        edges.add((first,second))
        if dfa.initial_state == subpath[0] :
            edges.add((special_state,first))
        if dfa.is_accepting(subpath[-1]):
            edges.add((second,special_state))
    return nodes, edges
    
import pandas as pd

def cost_matrix(abstraction1_edges,abstraction2_edges, cost_funct):
    abstraction1_edges = list(abstraction1_edges)
    abstraction2_edges = list(abstraction2_edges)
    matrix = dict()
    for e1 in abstraction1_edges:
        e1_row = []
        for e2 in abstraction2_edges:
            e1_row.append(cost_funct(e1,e2))
        matrix[e1] =  e1_row
    matrix = pd.DataFrame.from_dict(matrix,orient='index', columns=abstraction2_edges)
    '''
    #old code: using integer instead of float64 is better
    if cost_funct == levenshtein:
        #normalize matrix, i.e. divide by maximum of whole matrix
        matrix = matrix / max(matrix.max(0))
    '''
    '''
    #old code: more efficient to assign later 1s to the non assigned rows
    #add columns of 1s
    n_row, n_col = matrix.shape
    if n_col<n_row:
        for i in range(n_row-n_col):
            matrix['eps'+str(i)]= 1
    '''
    return matrix
    
from enchant.utils import levenshtein
from scipy.optimize import linear_sum_assignment
import numpy as np

def cost_funct_b(str1,str2): #Boolean cost function
    return 1-(str1==str2)

def recall(log,process):
    log_nodes, log_edges = log_abstraction(log,k)
    process_nodes, process_edges= process_abstraction(process,k)
    freqs = edges_freq(log_edges,log,k)
    matrix = cost_matrix(log_edges,process_edges,cost_funct_b)
    row_ind, col_ind = linear_sum_assignment(matrix)
    np_matrix = np.array(matrix)
    row_names = matrix.index.values
    den = sum(freqs[log_edge] for log_edge in log_edges)
    num1 = sum(np_matrix[i,col_ind[i]]*freqs[row_names[i]] for i in row_ind)
    num2 = den - sum(freqs[row_names[i]] for i in row_ind)
    num = num1 + num2
    return 1-num/den
    
import sys

if __name__ == "__main__":
	log_file = sys.argv[1]
	log = read_log(log_file)
	process_file = sys.argv[2]
	process = dot2dfa(process_file)
	alphabet_file = sys.argv[3]
	alphabet = read_alphabet(alphabet_file)
	process = complement(process,alphabet)
	k = int(sys.argv[4])
	rec = recall(log, process)
	print(rec)
        

