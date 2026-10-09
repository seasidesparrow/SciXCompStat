import os

def makeListDict(inputdict, key, value):
    if not inputdict.get(key, None):
        inputdict[key] = [value]
    else:
        inputdict[key].append(value)

def read_stem2set(filename):
    stem2set = {}
    if os.path.exists(filename):
        with open(filename, "r") as fi:
            for l in fi.readlines():
                l=l.strip()
                if l and l[0] != "#":
                    pair = l.split("\t")
                    if len(pair) > 1:
                        bibstem = pair[0]
                        setid = pair[1]
                        makeListDict(stem2set, bibstem, setid)
                    else:
                        print("Badly formatted line: %s" % l)
    else:
        print("Why you no give valid filename? %s" % filename)
    return stem2set
        
