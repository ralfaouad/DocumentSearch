import nltk
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

vocab = {}
vectors = []

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

def term_count_vectorizer(arr):
    # Equivalent to term count
    # ! Create the transform
    vectorizer = CountVectorizer()
    # ! Tokenize and build vocab
    vectorizer.fit(arr) 
    # ! Summarize
    print(vectorizer.vocabulary_) 
    # ! Encode the document
    vector = vectorizer.transform(arr) 
    return vector

def TF_IDF(arr):
    # ! Create the transform
    vectorizer = TfidfVectorizer()
    # ! Tokenize and build vocab
    vectorizer.fit(arr) 
    # ! Summarize
    vocab = vectorizer.vocabulary_
    print(vectorizer.vocabulary_)
    # ! Encode the document
    csr_matrices = vectorizer.transform(arr)
    vectors = csr_matrices.toarray()
    doc_term_matrix = csr_matrices.todense()
    print(doc_term_matrix)

    # print table
    df = pd.DataFrame(doc_term_matrix, columns=vectorizer.get_feature_names_out())
    print(df)

    return csr_matrices # >>> CSR matrices will be the input for the sim measures