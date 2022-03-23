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

from utils import process_words, remove_metadata, editDistance    

def and_merge(post_list1, post_list2):
    """Return result of AND operation on two posting lists"""
    ans = []
    ptr1 = 0 ; ptr2 = 0
    comparisons = 0
    while ptr1 < len(post_list1) and ptr2 < len(post_list2):
        
        if post_list1[ptr1] == post_list2[ptr2]:
            ans.append(post_list1[ptr1])
            ptr1 += 1
            ptr2 += 1
        elif post_list1[ptr1] < post_list2[ptr2] :
            ptr1 += 1
        else :
            ptr2 += 1
        comparisons += 1
    return ans, comparisons

def or_merge(post_list1, post_list2):
    """Return result of OR operation on two posting lists"""
    ans = []
    ptr1 = 0 ; ptr2 = 0
    comparisons = 0
    while ptr1 < len(post_list1) and ptr2 < len(post_list2):

        if post_list1[ptr1] == post_list2[ptr2]:
            ans.append(post_list1[ptr1])
            ptr1 += 1
            ptr2 += 1
        elif post_list1[ptr1] < post_list2[ptr2] :
            ans.append(post_list1[ptr1])
            ptr1 += 1
        else :
            ans.append(post_list2[ptr2])
            ptr2 += 1
        comparisons += 1
        
    while(ptr1 < len(post_list1)):
        ans.append(post_list1[ptr1])
        ptr1 += 1

    while(ptr2 < len(post_list2)):
        ans.append(post_list2[ptr2])
        ptr2 += 1
        
    return ans, comparisons


def not_merge(post_list1,doc_ID):
    """Return result of NOT operation on posting list"""
    result = []
    for doc in range(1,doc_ID):
        if doc not in post_list1 :
            result.append(doc)

    return result

def retrieve_list(term,temp_results=None):
    ans = []
    if term in index_dict.keys():
        ans = index_dict[term]
    elif term in temp_results.keys():
        ans = temp_results[term]
    else :
        print("###############################################")
        print(f'Error! Given term not found: {term}\n')
        print('Looking for alternatives...')
        suggestions = suggestEdits(term)
        print(f'\nDid you mean {suggestions[0]}, {suggestions[1]} or {suggestions[2]}?')
        print("###############################################")
        exit(0)
    return ans

def suggestEdits(word):
    dists = []
    for idx in tqdm(list(index_dict.keys())):
        if idx[0]==word[0]:
            dists.append(editDistance(idx, word, len(idx), len(word)))
        else:
            dists.append(np.inf)
    dists = np.array(dists)
    min_idxs = np.argpartition(dists, 3)[:3]
    all_words = list(index_dict.keys())
    suggestions = (all_words[min_idxs[0]], all_words[min_idxs[1]], all_words[min_idxs[2]])
    return suggestions


def processing_not_operator(query):
    temp_results = {}
    ind = 0
    i = len(query) - 1
    while i >= 0:
        if query[i] == 'not' :
            if query[i-1] == 'not':
                del query[i]
                del query[i-1]
                i -= 1
            else:
                term = query[i+1]
                post_list = retrieve_list(term,temp_results)
                key = 'result'+str(ind)
                ind += 1
                result = not_merge(post_list, doc_ID)
                temp_results[key] = result

                query[i] = key
                del query[i+1]
        i -= 1
    return query, temp_results, ind

def process_MIX(query, temp_results, ind):
    
    comparisons = 0
    while True:
        
        if 'and' in query:
            index = query.index('and')
            term1 = query[index-1]
            term2 = query[index+1]

            list1 = retrieve_list(term1, temp_results)
            list2 = retrieve_list(term2, temp_results)

            res,comp = and_merge(list1, list2)
            comparisons += comp
            key = 'result'+str(ind)
            ind += 1
            temp_results[key] = res
            query[index] = key
            del query[index-1]
            del query[index] # because of re arrangement
            # print(query)
            
        else :
            
            query = [term for term in query if term != 'or']
            while len(query) > 1:
                term1 = query[0]
                term2 = query[1]
                list1 = retrieve_list(term1, temp_results)
                list2 = retrieve_list(term2, temp_results)
                
                res,comp = or_merge(list1, list2)
                comparisons += comp
                
                key = 'result'+str(ind)
                ind += 1
                temp_results[key] = res
                query[0] = key
                del query[1]
            break
    results = retrieve_list(query[0], temp_results)
    return results,comparisons
            

 

def all_and_operators(query):
    ans = True
    if 'or' in query :
        ans = False
    return ans
            
def find_minimum(lists):
    
    dummy = lists.copy()
    pos1 = lists.index(min(lists))
    del dummy[pos1]
    sec_min = min(dummy)
    pos2 = lists.index(sec_min)
    
    return pos1,pos2

def optimised_AND(query, temp_results, ind):
    results = []
    comparisons = 0
    if len(query) == 0 :
        print('Nothing to Process')
    else :
        query = [term for term in query if term != 'and']
        posts_length = []
        for term in query:
            posts_length.append(len(retrieve_list(term,temp_results)))
        
        while True :
            
            if len(query) == 1:
                results = retrieve_list(query[0], temp_results)
                break
        
            else :
                print(posts_length)
                pos1,pos2 = find_minimum(posts_length)
                list1 = retrieve_list(query[pos1], temp_results)
                list2 = retrieve_list(query[pos2], temp_results)
                
                res,comp = and_merge(list1, list2)
                comparisons += comp
                key = 'result'+str(ind)
                ind += 1
                temp_results[key] = res
                posts_length[pos1] = len(res)
                query[pos1] = key
                
                del posts_length[pos2]
                del query[pos2]
    
    return results,comparisons
    
def process_query(query):
    
    temp_results = {}
    results = []
    query = process_words(query)
    query, temp_results, ind = processing_not_operator(query)
    
    if all_and_operators(query) :
        results,comparisons = optimised_AND(query,temp_results, ind)
        
    else :
        results,comparisons = process_MIX(query, temp_results, ind)
        
    return results
def print_results(results):
    docs = len(results)
    print("###############################################")
    print('Total Documents Retrieved are : {}\n'.format(docs))
    if(docs != 0):
        print('Result found in documents with IDs:')
        for num in results:
            print(num, end=" ")
    print("\n")
    files = []
    for id in results:
        files.append(file_mapper[id])
    return files   

# class TermNotFoundError(Exception):
#     def __init__(self, term):
#         self.term = term
#         self.message = ""
    


with open("inverted_index.pkl", "rb") as p:
    index_dict = pickle.load(p)
p.close()

with open("file_mapper.pkl", "rb") as fm:
    file_mapper = pickle.load(fm)
fm.close()

query = input("Enter the query to be found\n")
query_start_time = time()
query = query.split()
results = process_query(query)
query_end_time = time()
files = print_results(results)
if(len(files)>0):
    print(f"Query retrieved in {query_end_time-query_start_time} seconds")
print("###############################################")


