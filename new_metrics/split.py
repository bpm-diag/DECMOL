import datetime
import time

import sys
import pm4py
from pm4py.objects.log.obj import EventLog

log_name=sys.argv[1]
log_folder=sys.argv[2]

log_file = log_folder+log_name+".xes"
log = pm4py.read_xes(log_file)
traces = []
duration = []
tracesAsIs = []

for trace_log in log:
    trace = []
    for event in trace_log:
        trace.append(event['concept:name']) #should I use instead the pair (concept:name,lifecycle:transition)?
    traces.append(trace)
    tracesAsIs.append(trace_log)
    last = trace_log[-1]['time:timestamp']
    init = trace_log[0]['time:timestamp']
    duration.append((last-init).total_seconds())

print("total# of traces: "+str(len(traces)))
#print(traces)

#Remove duplicate traces. Note: only the first trace is keept
norep_traces = []
norep_tracesAsIs = []
norep_duration = []

for i in range(len(traces)):
    trace = traces[i]
    if not trace in norep_traces:
        norep_traces.append(trace)
        norep_tracesAsIs.append(tracesAsIs[i])
        norep_duration.append(duration[i])

print("total# of traces (no duplicates): "+str(len(norep_tracesAsIs)))

#compute average duration
avg_dur = sum(norep_duration)/len(norep_duration) #should we use median instead?
conversion = datetime.timedelta(seconds=avg_dur)
print("avg duration: "+str(conversion))

log_positive = EventLog()
log_negative = EventLog()
positive = []
negative = []
for i in range(len(norep_tracesAsIs)):
    dur = norep_duration[i]
    trace = norep_tracesAsIs[i]
    trace2 = norep_traces[i]
    if dur < avg_dur:
        log_positive.append(trace)
        positive.append(trace2)
    else:
        log_negative.append(trace)
        negative.append(trace2)


print("total# of traces (log+): "+str(len(log_positive)))
print("total# of traces (log-): "+str(len(log_negative)))

time.sleep(1)
pm4py.write_xes(log_positive,log_folder+log_name+'_positive.xes')
pm4py.write_xes(log_negative,log_folder+log_name+'_negative.xes')
with open(log_folder+log_name+'_positive.txt', 'w') as f:
    for _list in positive:
        concat = ""
        for _string in _list:
            concat += _string.replace(" ", "").lower()+" "
        concat = concat[:-1]
        f.write(concat)
        f.write('\n')
with open(log_folder+log_name+'_negative.txt', 'w') as f2:
    for _list in negative:
        concat = ""
        for _string in _list:
            concat += _string.replace(" ", "").lower()+" "
        concat = concat[:-1]
        f2.write(concat)
        f2.write('\n')
