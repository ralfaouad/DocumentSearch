# import VSM, json, path, utils, TED, os
# import xml.etree.ElementTree as ET
#! from spellchecker import SpellChecker

import VSM, json, path, utils, TED, os
import xml.etree.ElementTree as ET


directory = "Documents"
corpus = [os.path.join(directory,document) for document in os.listdir(directory)]


def corrector(query):
    spell = SpellChecker()
    misspelled = spell.unknown(query.split())

    for word in misspelled:
        query = query.replace(word, spell.correction(word))

    return query

# print(corrector("enfineerinf"))

def IR_with_indexing(query, method):
    query = utils.clean_text(query)
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
    query = utils.clean_text(query)
    # TFq = VSM.TF(query)
    sims = {}

    for doc in corpus:
    #     sims[doc] = VSM_query(query, doc, method)
    # tr = {x:y for x,y in sims.items() if y!= 0}
    # return tr
        sims[doc] = VSM_query(query, doc, method, False)

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
                    vectord.append(TFd[dimension] * VSM.IDFq(dimension))
                else: vectord.append(0.0)
            else:
                if(dimension in TFd):
                    vectord.append(TFd[dimension] * VSM.IDF(dimension, corpus, input="xml", approach="TB")) # No referring to indexing table
                else: vectord.append(0.0)

    # print(dimensions)
    # print(vectorq)
    # print(doc, vectord)
    return utils.cosine(vectorq, vectord) # modify cosine to take sim of contexts by WF

# user = input("Enter query: ")
# method = input("Enter 1 for TF, or 2 for TF-IDF")

# print(IR_with_indexing("hh", 1))
# print(IR_with_indexing("John", 1))

# print(IR_with_indexing(user, method))

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
    
# print(IR_with_indexing("John", 1))

# print(KNN(3,))
# print(KNN_range(2,1,{'gfg' : 10, 'is' : 1, 'best' : 45, 'for' : 4, 'CS' : 5}))
