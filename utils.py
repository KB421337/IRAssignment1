import nltk
from nltk import word_tokenize


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import os
from time import time

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# and, or, not - boolean operators
stop_words.remove('and')
stop_words.remove('or')
stop_words.remove('not')

def remove_metadata(lines):
    """Remove metadata from text lines"""
    for i in range(len(lines)):
        if lines[i] == '\n':
            start = i + 1
            break
    return lines[start:]
                
def process_words(words):
    """
    Process each individual word. Removes extra characters and convert words to lowercase. 
    Uses lemmatization and does not add to inverted index if result is a stopword
    """
    mod_words = []
    symbols = [ "'",'/','.','-','!','@','#','$','^','&','*','(',')','+']
    removed_symbols = []
    for word in words :
        for sym in symbols:
            if sym in word:
                word = word.replace(sym,'')
        removed_symbols.append(word)
        
    words = removed_symbols
    del removed_symbols
        
    for word in words:
        word = word.lower()   # Convert to lowercase
        if word.isalpha():
            word = lemmatizer.lemmatize(word) # Lemmatization
            if word not in stop_words and len(word) >= 2: # Check if word is stopword
                mod_words.append(word)
    return mod_words

def editDistance(str1, str2, m, n):
    """Find edit distance between two strings str1 and str2"""

    if m == 0:
        return n
    if n == 0:
        return m
 
    if str1[m-1] == str2[n-1]:
        return editDistance(str1, str2, m-1, n-1)

    return 1 + min(editDistance(str1, str2, m, n-1),    # Insert
                   editDistance(str1, str2, m-1, n),    # Remove
                   editDistance(str1, str2, m-1, n-1)    # Replace
                   )

