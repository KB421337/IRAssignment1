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

from utils import remove_metadata, process_words

def process_text(lines, index_dict, doc_ID):
    """Preprocess the text and create inverted index"""
    lines = remove_metadata(lines)  # Remove metadata
    seperator = ' '
    file = seperator.join(lines)
    words = word_tokenize(file)     # Tokenize text
    words = process_words(words)    # Process words
    words = sorted(words)           # Sort the tokens
    
    for word in words:
        if word in index_dict.keys():
            if doc_ID not in index_dict[word]:
                index_dict[word].append(doc_ID)
        else:
            index_dict[word] = [doc_ID]
    
    return index_dict

def main():
    """Main function"""

    file_mapper = {}  # Maps file from docID to name of file
    root_dir = '../shakespeares_works'
    doc_ID = 1
    index_dict = {}

    print("\n###############################################")
    print("Reading from data folder, found these documents")
    print("###############################################\n")
    
    preprocess_start = time()
    for fil in os.listdir(root_dir): # for each file
        print(fil)
        file_path = os.path.join(root_dir,fil) 

            
        with open(file_path, 'r') as f:
            lines = f.readlines()
            file_mapper[doc_ID] = file_path
            index_dict = process_text(lines, index_dict,doc_ID)
            doc_ID += 1

    with open("InvertedIndex.txt", "w") as file:
        for key in sorted(index_dict):
            file.write(key)
            file.write(" ")
            value = ','.join(str(v) for v in index_dict[key])
            file.write(value)
            file.write("\n")
        print("\n###############################################")
        print("Created Inverted Index")
        file.close()
    
    def rotate(str, n):
        return str[n:] + str[:n]

    with open("PermutermIndex.txt","w") as perm:
        keys = index_dict.keys()
        for key in sorted(keys):
            dkey = key + "$"
            for i in range(len(dkey),0,-1):
                out = rotate(dkey,i)
                perm.write(out)
                perm.write(" ")
                perm.write(key)
                perm.write("\n")
    perm.close()

    print("Created Permuterm Index")
    print("###############################################\n")

    with open("inverted_index.pkl", "wb") as p:
        pickle.dump(index_dict, p)
    p.close()

    with open("file_mapper.pkl", "wb") as fm:
        pickle.dump(file_mapper, fm)
    fm.close()

    f.close()


if __name__ == "__main__":
    main()
            
            
    