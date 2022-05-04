import VSM, json, path, utils, TED, os, math
import xml.etree.ElementTree as ET

directory = "Documents"
corpus = [os.path.join(directory,document) for document in os.listdir(directory)]

def IR_with_indexing(query, method):
    query = utils.clean_text(query)
    docs = set()
    sims = {}

    with open("IndexingTableTags.json",'r') as file:
        index = json.load(file)

    # BinarySearch for each term of the query in the Indexing Table
    for word in query.split():
        if utils.binarySearch(list(index.keys()),word) is not None:
            for doc in index[word]:
                docs.add(os.path.join("Documents",doc))
        else:
            print("Term not found")
        
    if(not docs): return None
    for doc in docs:
        sims[doc] = VSM_query(query, doc, method)
    return sims

def IR_without_indexing(query, method):
    query = utils.clean_text(query)
    sims = {}

    for doc in corpus:
        sims[doc] = VSM_query(query, doc, method, False)
        tr = {x:y for x,y in sims.items() if y!= 0}
    return tr

def IR_with_indexingXML(tree, method):
    tc = path.TC(tree)
    docs = set()
    sims = {}

    with open("IndexingTable.json",'r') as file:
        index = json.load(file)

    # BinarySearch for each term of the query in the Indexing Table
    for term in tc:
        if utils.binarySearch(list(index.keys()),term) is not None:
            for doc in index[term]:
                docs.add(os.path.join("Documents",doc))
        else:
            print("Term not found")
        
    if(not docs): return None
    for doc in docs:
        treeB = TED.preprocessing(ET.parse(doc).getroot())
        sims[doc] = VSM_qXML(tree, treeB, method)
    return sims

def IR_without_indexingXML(tree, method):
    sims = {}

    for doc in corpus:
        treeB = TED.preprocessing(ET.parse(doc).getroot())
        sims[doc] = VSM.VSM_xml(tree, treeB, corpus, method)

    return sims

def VSM_query(query, document, method, indexing=True):
    doc = open(document,'r')
    tree = TED.preprocessing(ET.parse(doc).getroot())

    TFq = VSM.TF(query)
    tb = path.tag_based(tree)
    TFd = VSM.TF(" ".join(tb))
    dimensions = list(TFq.keys() | TFd.keys())

    vectorq = []
    vectord = []

    if(method == 0):
        for dimension in dimensions:
            vectorq.append(TFq.get(dimension) or 0)
            vectord.append(TFd.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            vectorq.append(TFq.get(dimension) or 0)
            
            if(indexing):
                if(dimension in TFd):
                    vectord.append(TFd[dimension] * IDFq(dimension))
                else: vectord.append(0.0)
            else:
                if(dimension in TFd):
                    vectord.append(TFd[dimension] * VSM.IDF(dimension, corpus, input="xml", approach="TB")) # No referring to indexing table
                else: vectord.append(0.0)

    return utils.cosine(vectorq, vectord) # modify cosine to take sim of contexts by WF

def VSM_qXML(treeA, treeB, method):
    vector1 = []
    vector2 = []
    dimensions = {}
    # Content will be cleaned in the preprocessing

    tc1 = path.TC(treeA)
    tc2 = path.TC(treeB)

    TCF1 = VSM.TF(" ".join(tc1))
    TCF2 = VSM.TF(" ".join(tc2))
    dimensions = list(TCF1.keys() | TCF2.keys())

    if(method == 0):
        for dimension in dimensions:
            vector1.append(TCF1.get(dimension) or 0)
            vector2.append(TCF2.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            if(dimension in TCF1):
                vector1.append(TCF1[dimension] * IDFqxml(dimension))
            else: vector1.append(0.0)
            
            if(dimension in TCF2):
                vector2.append(TCF2[dimension] * IDFqxml(dimension))
            else: vector2.append(0.0)
    
    similarity = utils.e_cosine(dimensions, vector1, vector2)
    return similarity

def IDFq(term):
    occurrences = 0
    index = json.load(open("IndexingTableTags.json", 'r'))

    if(index[term] != None):
        occurrences = len(index[term])

    size= len([name for name in os.listdir("Documents") if os.path.isfile(os.path.join("Documents",name))])
    return math.log(size/occurrences,10)

def IDFqxml(term):
    occurrences = 0
    index = json.load(open("IndexingTable.json", 'r'))

    if(index[term] != None):
        occurrences = len(index[term])

    size= len([name for name in os.listdir("Documents") if os.path.isfile(os.path.join("Documents",name))])
    return math.log(size/occurrences,10)
    
def KNN(K,res):
    sorted_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1],reverse=True)}
    neighbors = dict(list(sorted_res.items())[0:K])
    return neighbors

def range(e, res):
    # if sim >= e add term to neighbors
    sorted_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1],reverse=True)}
    inrange = {}
    for k,v in sorted_res.items():
        if v>= e:
            inrange[k] = v
        else:
            break
    return inrange

def KNN_range(k, e, res):
    res1 = range(e,res)
    res2 = KNN(k,res1)
    return res2