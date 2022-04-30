import math, json, path, TED, utils
import xml.etree.ElementTree as ET
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def clean_text(text):
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Removing non alphabetic tokens
    words = [word for word in tokens if word.isalpha()]
    # Stop word removal
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(word) for word in words]
    return (" ").join(lemmatized)

def TF(text):
    TF = {}
    for word in text.split():
        if(word in TF):
            TF[word] += 1
        else:
            TF[word] = 1
    return TF

def IDF(term, corpus, input="xml"):
    occurrences = 0

    if input == "xml":
        for document in corpus:
            doc = open(document, 'r')
            tree = TED.preprocessing(ET.parse(doc).getroot())
            if(term in path.TC(tree)):
                occurrences += 1
    else:
        for document in corpus:
            with open(document,'r') as file:
                str = document.read()
            if(term in clean_text(str).split()):
                occurrences += 1

    print("log(",len(corpus),"/",occurrences,")")

    return math.log(len(corpus)/occurrences,10)

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
        dict = TF(clean_text(str))
    
    TF_IDF[term] = dict[term] * IDF(term, corpus)

    return TF_IDF[term]

def VSM_txt(text1, text2, corpus, i = 1, m = 0):
    # i: 0 (TF), 1 (TF IDF)
    vector1 = []
    vector2 = []
    dimensions = {}
    text1 = clean_text(text1)
    text2 = clean_text(text2)

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
                vector1.append(TF_IDF(dimension, corpus[0], corpus))
            else: vector1.append(0.0)
            
            if(dimension in TF2):
                vector2.append(TF_IDF(dimension, corpus[1], corpus))
            else: vector2.append(0.0)
    
        # print(dimensions)
        # print(vector1)
        # print(vector2)

def VSM_xml(treeA, treeB, corpus, i = 1, m = 0):
    vector1 = []
    vector2 = []
    dimensions = {}
    # Content will be cleaned in the preprocessing

    tc1 = path.TC(treeA)
    tc2 = path.TC(treeB)

    TCF1 = TF(" ".join(tc1))
    TCF2 = TF(" ".join(tc2))
    dimensions = TCF1.keys() | TCF2.keys()

    if(i == 0):
        for dimension in dimensions:
            vector1.append(TCF1.get(dimension) or 0)
            vector2.append(TCF2.get(dimension) or 0)
        
    else:
        for dimension in dimensions:
            if(dimension in TCF1):
                vector1.append(TF_IDF(dimension, corpus[0], corpus))
            else: vector1.append(0.0)
            
            if(dimension in TCF2):
                vector2.append(TF_IDF(dimension, corpus[1], corpus))
            else: vector2.append(0.0)

    print(dimensions)
    print("V1: ", vector1)
    print("V2: ", vector2)

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
   

# VSM text files
# with open("Documents/sample1.txt",'r') as file1:
#         str1 = file1.read()
# with open("Documents/sample2.txt",'r') as file2:
#         str2 = file2.read()

# print(VSM_txt(str1, str2, ["Documents/sample1.txt", "Documents/sample2.txt"], 1, 1))

# VSM XML
doc1 = open("Documents/XML1.xml", 'r')
doc2 = open("Documents/XML2.xml", 'r')

tree1 = TED.preprocessing(ET.parse(doc1).getroot())
tree2 = TED.preprocessing(ET.parse(doc2).getroot())

sim = VSM_xml(tree1, tree2, ["Documents/XML1.xml","Documents/XML2.xml"], 1, 0)
print(sim)



