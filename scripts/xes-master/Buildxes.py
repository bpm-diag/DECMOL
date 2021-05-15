import xes, os, sys

def log(pos, j, path):
    positive = open(pos,"r")
    lines = positive.readlines()
    t = []
    x = 0
    for line in lines:
        t.append([])
        line = line.strip()
        v = line.split(" ")
        for i in v:
            t[x].append({"concept:name":i, "lifecycle:transition":"complete"})
        x += 1

    log = xes.Log()
    i = 1
    for trace in t:
        t = xes.Trace()
        st = "case_"+str(i)
        a = xes.Attribute(type="string", key="concept:name", value=st)
        t.add_attribute(a)
        for event in trace:
            e = xes.Event()
            e.attributes = [
                xes.Attribute(type="string", key="concept:name", value=event["concept:name"]),
                xes.Attribute(type="string", key="lifecycle:transition", value=event["lifecycle:transition"])
            ]
            t.add_event(e)
        log.add_trace(t)
        i += 1
    log.classifiers = [
        xes.Classifier(name="concept:name",keys="concept:name")
    ]
    open(path+os.sep+"generalization"+os.sep+str(j)+os.sep+"positive.xes", "w").write(str(log))

if __name__ == "__main__":
    
    k = sys.argv[1:][0]
    path = sys.argv[1:][1]
    
    for i in range(int(k)):
        positive=path+os.sep+"generalization"+os.sep+str(i)+os.sep+"positive.txt"
        log(positive, i, path)


    