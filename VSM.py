from distutils.command.clean import clean
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

def TF(text):
    TF = {}
    for word in text.split():
        if(word in TF):
            TF[word] += 1
        else:
            TF[word] = 1
    return TF

def IDF(term, corpus):
    occurrences = 0

    for file in corpus:
        with open(file,'r') as file:
            str = file.read()
        if(term in clean_text(str).split()):
            occurrences += 1

    print("log(",len(corpus),"/",occurrences,")")

    return math.log(len(corpus)/occurrences,10)

def TF_IDF(term, document, corpus):
    dict = {}
    TF_IDF = {}

    with open(document,'r') as file:
        str = file.read()
    
    dict = TF(clean_text(str))
    TF_IDF[term] = dict[term] * IDF(term, corpus)

    return TF_IDF[term]

def VSM_txt(text1, text2, corpus, i = 1, m = 0):
    # i: 0 (TF), 1 (TF IDF)
    # m: 0 (cosine), 1 (pcc), 2 (euclidian), 3 (manhattan), 4 (tanimoto)
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
    
        print(dimensions)
        print(vector1)
        print(vector2)


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


print(VSM_txt(str1, str2, ["Documents/sample1.txt", "Documents/sample2.txt"], 1, 1))


