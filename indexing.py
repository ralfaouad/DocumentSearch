import os
import json, TED, path
import xml.etree.ElementTree as ET
import regex as re
from VSM import clean_text, TF
directory = 'C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 2/DocumentSearch/Documents'

indexing_table = {}
corpus_size = 0

def process_XML(filename):
    doc = open(directory + "/" + filename,'r')
    tree = TED.preprocessing(ET.parse(doc).getroot())

    terms = path.TC(tree)

    for term in terms:
        word = re.split(',',term)[0]
        pth = re.split(',',term)[1]
        if(word in indexing_table):
            if(filename in indexing_table[word]):
                indexing_table[word][filename].append(pth)
            else: indexing_table[word][filename] = [pth]
        else:
            indexing_table[word] = { filename : [pth] }

def process_TXT(filename):
    with open(directory + "/" + filename,'r') as file:
        str = file.read()

    terms = clean_text(str).split()
    term_freq = TF(" ".join(terms))

    for term in terms:
        if(term in indexing_table):
            indexing_table[term][filename] =  term_freq[term]
        else:
            indexing_table[term] = {filename : term_freq[term]}

def save_toJSON(indexing_table):
    with open('IndexingTable.json', 'w') as f:
        json.dump(indexing_table, f, indent=2)

# Add file to directory -> Update Indexing Table
def add(filename):
    process_XML(filename)
    save_toJSON(indexing_table)

# Delete file from directory -> Update Indexing Table
# def delete(filename):
#     for(key in indexing_table.keys()):
        
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        process_XML(filename)
        # corpus_size += 1


save_toJSON(indexing_table)

# for row in indexing_table.items():
#     print(row)


