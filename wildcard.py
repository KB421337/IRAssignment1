from cmath import inf
import nltk
from nltk import word_tokenize


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import os
from time import time
from nltk.corpus import stopwords
from tqdm import tqdm
import numpy as np  

def main():
    query = input('Enter Query : ')

    query_start = time()
    parts = query.split("*")

    if len(parts) == 3:
        case = 4
    elif parts[1] == '':
        case = 1
    elif parts[0] == '':
        case = 2
    elif parts[0] != '' and parts[1] != '':
        case = 3

    if case == 4:
        if parts[0] == '':
            case = 1

    inverted = {}
    with open('InvertedIndex.txt') as f:
        for line in f:
            temp = line.split( )
            val = temp[1].split(",")
            inverted[temp[0]] = val

    

    permuterm = {}
    with open('PermutermIndex.txt') as f:
        for line in f:
            temp = line.split( )
            permuterm[temp[0]] = temp[1]


    def prefix_match(term, prefix):
        term_list = []
        for tk in term.keys():
            if tk.startswith(prefix):
                term_list.append(term[tk])
        return term_list
            
    docID = 0

    def processQuery(query):    
        term_list = prefix_match(permuterm,query)
        #print(term_list)
        
        docID = []
        for term in term_list:
            docID.append(inverted[term])

        results = []
        for x in docID:
            for y in x:
                results.append(y)       

        results = [int(x) for x in results]
        query_end = time()
        results = sorted(list(set(results)))
        docs = len(results)

        print("###############################################")
        print('Total Documents Retrieved are : {}\n'.format(docs))
        if(docs != 0):
            print('Result found in documents with IDs:')
            for num in results:
                print(num, end=" ")
        print("\n")
        print(f"Query retrieved in {query_end-query_start} seconds")
        print("###############################################\n")
        return results

    if case == 1:
        query = "$" + parts[0]
    elif case == 2:
        query = parts[1] + "$"
    elif case == 3:
        query = parts[1] + "$" + parts[0]
    elif case == 4:
        queryA = parts[2] + "$" + parts[0]
        queryB = parts[1]

    # print(query)
    def bitwise_and(A,B):
        return set(A).intersection(B)
        
    if case != 4:
        processQuery(query)
    elif case == 4:
    # queryA Z$X
        term_list = prefix_match(permuterm,queryA)
        #print(term_list)
        
        docID = []
        for term in term_list:
            docID.append(inverted[term])
        #print(docID)

        temp1 = []
        for x in docID:
            for y in x:
                temp1.append(y)
        #print(temp)        

        temp1 = [int(x) for x in temp1]
    # queryB Y
        term_list = prefix_match(permuterm,queryB)
        #print(term_list)
        
        docID = []
        for term2 in term_list:
            docID.append(inverted[term2])
        #print(docID)

        temp2 = []
        for x in docID:
            for y in x:
                temp2.append(y)
        #print(temp)        

        temp2 = [int(x) for x in temp2]


        results = bitwise_and(temp1,temp2)
        query_end = time()
        results = sorted(list(set(results)))
        docs = len(results)
        print("###############################################")
        print('Total Documents Retrieved are : {}\n'.format(docs))
        if(docs != 0):
            print('Result found in documents with IDs:')
            for num in results:
                print(num, end=" ")
        print("\n")
        print(f"Query retrieved in {query_end-query_start} seconds")
        print("###############################################\n")

if __name__ == "__main__":
    main()
