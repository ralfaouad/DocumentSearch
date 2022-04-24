import nltk
import math
import json
import os
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
    # ! Tokenization
    tokens = word_tokenize(text)
    # ! Removing non alphabetic tokens
    words = [word for word in tokens if word.isalpha()]
    # ! Stop word removal
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # ! Stemming
    # porter = PorterStemmer()
    # stemmed = [porter.stem(word) for word in words]
    # ! Lemmatization
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(word) for word in words]
    return (" ").join(lemmatized)

def TF(str):
    TF = {}
    for word in str.split():
        if(word in TF):
            TF[word] += 1
        else:
            TF[word] = 1
    return TF

def IDF(term, corpus_path):
    occurrences = 0
    size = 0

    for filename in os.listdir(corpus_path):
        size += 1
        with open(corpus_path + "/" + filename,'r') as file:
            str = file.read()
        # str = clean_text(str) 

        if(term in str.split()):
            occurrences += 1

    print("log(",size,"/",occurrences,")")
    return math.log(size/occurrences,10)

def TF_IDF(term, document, corpus_path):
    dict = {}
    TF_IDF = {}

    with open(corpus_path + "/" + document,'r') as file:
            str = file.read()
    
    dict = TF(str)
    TF_IDF[term] = dict[term] * IDF(term, corpus_path)

    return TF_IDF[term]

# Insert here Vectorizing function

# def TF2(arr):
#     # Equivalent to term count
#     # ! Create the transform
#     vectorizer = CountVectorizer()
#     # ! Tokenize and build vocab
#     vectorizer.fit(arr) 
#     # ! Summarize
#     print(vectorizer.vocabulary_) 
#     # ! Encode the document
#     vector = vectorizer.transform(arr) 
#     return vector

# def TF_IDF(arr):
#     # ! Create the transform
#     vectorizer = TfidfVectorizer()
#     # ! Tokenize and build vocab
#     vectorizer.fit(arr) 
#     # ! Summarize
#     vocab = vectorizer.vocabulary_
#     print(vectorizer.vocabulary_)
#     # ! Encode the document
#     csr_matrices = vectorizer.transform(arr)
#     vectors = csr_matrices.toarray()
#     doc_term_matrix = csr_matrices.todense()
#     print(doc_term_matrix)

    # print table
    # df = pd.DataFrame(doc_term_matrix, columns=vectorizer.get_feature_names_out())
    # print(df)

    # return csr_matrices # >>> CSR matrices will be the input for the sim measures


# VSM text files
with open("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 2/DocumentSearch/Documents/sample1.txt",'r') as file1:
        str1 = file1.read()

with open("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 2/DocumentSearch/Documents/sample2.txt",'r') as file2:
        str2 = file2.read()

data1 = clean_text(str1)
data2 = clean_text(str2)
print(data1)
print(data2)

print(TF(data1))
print(TF(data2))

