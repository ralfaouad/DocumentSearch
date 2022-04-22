import TED
import VSM
import xml.etree.ElementTree as ET
from utils import cosine, euclidian, manhattan, tanimoto

#TED
# TODO replace both document with input from GUI
with open("Documents/XML1.xml",'r') as file1:
    str1 = file1.read()
with open("Documents/XML2.xml",'r') as file2:
    str2 = file2.read()

tree1 = ET.fromstring(str1)
tree2 = ET.fromstring(str2)

doc1 = TED.preprocessing(tree1)
doc2 = TED.preprocessing(tree2)

print("TED Similarity: ",TED.TED(doc1,doc2))

# doc1 = TED.preprocessing(ET.parse(open("Documents/XML1.xml",'r')).getroot())
# doc2 = TED.preprocessing(ET.parse(open("Documents/XML2.xml",'r')).getroot())
# print("TED Similarity: ",TED.TED(doc1,doc2))

# ! i) text document pre-processing
# ? In this step, we will be differenciating between input XML file and textual files/simple queries.
# * If input is XML 
#  TODO using XML validator
# * If input is .txt/query
#  TODO

def isXML(value):
    try:
        ET.fromstring(value)
    except ET.ParseError:
        return False
    return True

# print(isXML(str1))


# ! ii) document vector representation
# ? In this step, we will be transforming each document to a vector representation.
# ? But first, we need to tokenize, stem, lemmatize

# cleaned = VSM.clean_text("This is Sara. Sara is having the best IDPA experience!")
# print(cleaned)
# vectorized = VSM.vectorizer(cleaned)
# print(vectorized)
# # print([e for e in arr])


# TODO add clean method before TF-IDF step
output = VSM.TF_IDF(["the quick brown fox jumped over the lazy dog", "the dog", "the fox"])

# cosim = cosine(output[0],output[1])
# print(cosim)

# pcc = tanimoto(output[0],output[1])
# print(pcc)

# ? Optional: User can choose which of the following 3 approches to use
# TODO
# * Augmented Vectors
# TODO
# * Term-context
# TODO
# * Matrix model

# ! iii) term weighing and iv) document vector similarity evaluation
# ? In this step, we will be computing the vectors and their dimensions
###
# ? Needed: User can choose which of the following to activate/deactivate.
# * TF
# TODO
# * IDF
# TODO
# * TF-IDF
# TODO
###
# ? Needed: User can choose which measure to use.
# * Cosine
# TODO
    

# * PCC
# TODO
# * Euclidian, Manhattan, Tanimoto & Dice

# ! v) comparison with project #1's TED measure
# ? In this step, we will compare TED and IR in terms of:
# * Time performance
# TODO
# * Quality performance
# TODO

# ! vi) building index structure
# ? In this step, we will build the inverted indexing technique
# * Add To indexing table
# TODO
# * Run against current indexing table

# ! vii) using querying interface
# ? This step can be merged to step i)
# TODO
