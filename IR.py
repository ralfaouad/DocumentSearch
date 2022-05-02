import VSM, json, path, utils, TED, os
import xml.etree.ElementTree as ET

corpus = ["Documents/XML1.xml", "Documents/XML2.xml","Documents/XML3.xml"]

def IR_with_indexing(query, method):
    # query = VSM.clean_text(query)
    docs = set()
    sims = {}

    with open("IndexingTable.json",'r') as file:
        index = json.load(file)

    # for word in query.split():
    #     if(word in index.keys()):    # Suggestion: Binary Search for optimzation
    #         for doc in index[word].keys():
    #             docs.add(os.path.join("Documents", doc))

    # BinarySearch for each term of the query in the Indexing Table
    for word in query.split():
        if utils.binarySearch(list(index.keys()),word) is not None:
            for doc in index[word].keys():
                docs.add(os.path.join("Documents",doc))
        else:
            print("Term not found")
        
    if(not docs): return None
    for doc in docs:
        sims[doc] = VSM_query(query, doc, method)

    return sims

def IR_without_indexing(query, method):
    # query = VSM.clean_text(query)
    # TFq = VSM.TF(query)
    sims = {}

    for doc in corpus:
        sims[VSM_query(query, doc, method)] = doc

    return sims
        
def VSM_query(query, document, method):

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
            
            if(dimension in TFd):
                vectord.append(TFd[dimension] * VSM.IDF(dimension, corpus, "xml", "TB"))
            else: vectord.append(0.0)

    print(dimensions)
    print(vectorq)
    print(doc, vectord)
    return utils.cosine(vectorq, vectord) # modify cosine to take sim of contexts by WF

# user = input("Enter query: ")
# method = input("Enter 1 for TF, or 2 for TF-IDF")

# print(IR_with_indexing("hh", 1))
