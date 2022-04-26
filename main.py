import TED
import VSM
import xml.etree.ElementTree as ET
from utils import cosine, euclidian, manhattan, tanimoto

# Similarity between 2 Docs
# TODO replace both document with input from GUI

with open("Documents/XML1.xml",'r') as file1:
    str1 = file1.read()
with open("Documents/XML2.xml",'r') as file2:
    str2 = file2.read()

if(file1.endswith(".xml") and file2.endswith(".xml")):
    treeA = TED.preprocessing(ET.parse("XML1.xml").getroot())
    treeB = TED.preprocessing(ET.parse("XML2.xml").getroot())
    print("N&J Similarity: ", TED.TED(treeA, treeB))
    print("VSM Similarity: ") # VSM EXTENDED TO XML

else:
    print("WF Similarity: ")
    print("VSM Similarity: ") # VSM Normal


# tree1 = ET.fromstring(str1)
# tree2 = ET.fromstring(str2)


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

# TODO add clean method before TF-IDF step
print(VSM.TF(["the quick brown fox jumped over the lazy dog"]))

# cosim = cosine(output[0],output[1])
# print(cosim)

# pcc = tanimoto(output[0],output[1])
# print(pcc)
# print(VSM.TF_IDF(["the quick brown fox jumped over the lazy dog", "the dog", "the fox"]))

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
