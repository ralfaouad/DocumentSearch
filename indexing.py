import os
import json
from VSM import clean_text, TF
directory = 'C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 2/DocumentSearch/Documents'

indexing_table = {}
corpus_size = 0

def process(filename):
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
    process(filename)
    save_toJSON(indexing_table)

# Delete file from directory -> Update Indexing Table
# def delete(filename):
#     for(key in indexing_table.keys()):
        
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
      process(filename)
      corpus_size += 1
      continue
    else:
        continue
save_toJSON(indexing_table)

# for row in indexing_table.items():
#     print(row)


