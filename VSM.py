import math, path, TED, utils
import xml.etree.ElementTree as ET
import pandas as pd

def TF(str):
    TF = {}
    for term in str.split():
        if(term in TF):
            TF[term] += 1
        else:
            TF[term] = 1
    return TF

def IDF(term, corpus, input="xml", approach="TC"):
    occurrences = 0

    if input == "xml": # XML Input
        for document in corpus:
            doc = open(document, 'r')
            tree = TED.preprocessing(ET.parse(doc).getroot())

            if approach == "TC": # Term Context Approach
                if(term in path.TC(tree)):
                    occurrences += 1
            else:
                if(term in path.tag_based(tree)): # Tag Based Approach (when dealing with query)
                    occurrences += 1
    else: # Text Input
        for document in corpus:
            with open(document,'r') as file:
                str = file.read()
            if(term in utils.clean_text(str).split()):
                occurrences += 1

    return math.log((len(corpus)+1)/occurrences,10) # Adding 1 to the size of corpus <=> Adding dummy file

def TF_IDF(term, document, corpus, input="xml"):
    dict = {}
    TF_IDF = {}

    if input == "xml":
        doc = open(document, 'r')
        tree = TED.preprocessing(ET.parse(doc).getroot())
        dict = TF((" ").join(path.TC(tree)))
    else:
        with open(document,'r') as file:
            str = file.read()
        dict = TF(utils.clean_text(str))
    
    TF_IDF[term] = dict[term] * IDF(term, corpus, input)

    return TF_IDF[term]

def VSM_txt(text1, text2, corpus, i = 1, m = 0):
    # i: 0 (TF), 1 (TF IDF)
    vector1 = []
    vector2 = []
    dimensions = {}
    text1 = utils.clean_text(text1)
    text2 = utils.clean_text(text2)

    TF1 = TF(text1)
    TF2 = TF(text2)
    dimensions = TF1.keys() | TF2.keys()
    if(i == 0):
        for dimension in dimensions:
            vector1.append(TF1.get(dimension) or 0)
            vector2.append(TF2.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            if(dimension in TF1):
                vector1.append(TF_IDF(dimension, corpus[0], corpus, "text"))
            else: vector1.append(0.0)
            
            if(dimension in TF2):
                vector2.append(TF_IDF(dimension, corpus[1], corpus, "text"))
            else: vector2.append(0.0)

    df = pd.DataFrame(list(zip(vector1, vector2)), index = dimensions, columns =['Vector1', 'Vector2'])
    print("Original DataFrame :")
    df
    
    if m == 0:
        similarity = utils.cosine(vector1, vector2)
    elif m == 1:
        similarity = utils.PCC(vector1, vector2)
    elif m == 2:
        similarity = utils.euclidian(vector1, vector2)
    elif m == 3:
        similarity = utils.manhattan(vector1, vector2)
    elif m == 4:
        similarity = utils.jaccard(vector1, vector2)
    else: similarity = utils.dice(vector1, vector2)
    
    return similarity

def VSM_xml(treeA, treeB, corpus, i = 1, m = 0):
    vector1 = []
    vector2 = []
    dimensions = {}
    # Content was cleaned in the preprocessing

    tc1 = path.TC(treeA)
    tc2 = path.TC(treeB)

    TCF1 = TF(" ".join(tc1))
    TCF2 = TF(" ".join(tc2))
    dimensions = list(TCF1.keys() | TCF2.keys())

    if(i == 0):
        for dimension in dimensions:
            vector1.append(TCF1.get(dimension) or 0)
            vector2.append(TCF2.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            if(dimension in TCF1):
                vector1.append(TCF1[dimension] * IDF(dimension, corpus))
            else: vector1.append(0.0)
            
            if(dimension in TCF2):
                vector2.append(TCF2[dimension] * IDF(dimension, corpus))
            else: vector2.append(0.0)

    df = pd.DataFrame(list(zip(vector1, vector2)), index = dimensions, columns =['Vector1', 'Vector2'])
    print("Original DataFrame :")
    df

    if m == 0:
        similarity = utils.e_cosine(dimensions, vector1, vector2)
    elif m == 1:
        similarity = utils.PCC(vector1, vector2)
    elif m == 2:
        similarity = utils.euclidian(vector1, vector2)
    elif m == 3:
        similarity = utils.manhattan(vector1, vector2)
    elif m == 4:
        similarity = utils.jaccard(vector1, vector2)
    else: similarity = utils.dice(vector1, vector2)

    return similarity

