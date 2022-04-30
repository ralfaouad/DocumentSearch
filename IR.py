import VSM, json, path, utils, TED
import xml.etree.ElementTree as ET

corpus = ["Documents/XML1.xml", "Documents/XML2.xml"]

def IR_with_indexing(query, method):
    query = VSM.clean_text(query)
    docs = ()
    sims = {}

    with open("IndexingTable.json",'r') as file:
        index = json.load(file)

    for word in query.split():
        if(index[word]):    # Suggestion: Binary Search for optimzation
            docs.add(index[word])

    for doc in docs:
        sims[VSM(query, doc, method)] = doc

    return sims

def IR_without_indexing(query, method):
    # query = VSM.clean_text(query)
    TFq = VSM.TF(query)
    sims = {}

    for doc in corpus:
        sims[VSM(query, doc, method)] = doc

    return sims
        
def VSM(query, document, method):

    doc = open(document,'r')
    tree = TED.preprocessing(ET.parse(doc).getroot())

    TFq = VSM.TF(query)
    TFd = VSM.TF(" ".join(path.TC(tree)))
    dimensions = TFq.keys() | TFd.keys()

    vectorq = []
    vectord = []

    if(method == 0):
        for dimension in dimensions:
            vectorq.append(TFq.get(dimension) or 0)
            vectord.append(TFd.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            vectorq.append(TFq.get(dimension) or 0)
            
            if(dimension in TFd):
                vectord.append(VSM.TF_IDF(dimension, doc, corpus))
            else: vectord.append(0.0)

    print(dimensions)
    print(vectorq)
    print(vectord)
    return utils.cosine(vectorq, vectord) # modify cosine to take sim of contexts by WF

user = input("Enter query: ")
method = input("Enter 1 for TF, or 2 for TF-IDF")

print(IR_with_indexing(user, method))
