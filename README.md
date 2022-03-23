# CS F469 – Information Retrieval
## Assignment-1: Boolean Retrieval System

Group members:
1. Sathvik Bhaskarpandit (2019A7PS1200H)
2. Kaustubh Bhanj (2019A7PS0009H)
3. Arnav J Pillai ()

*The repository contains the source code for a boolean information retrieval system for a set of Shakespeare's works.*

The following queries are supported:
- boolean queries with AND OR and NOT
- wildcard queries (for example ackn*)

### How to run the code

#### Step 1: Run indexer.py
Running the python file creates the inverted index and permuterm indexes and stores them in text files. Additionally, the inverted index dictionary and file mapper dictionary (which maps document ID to name of document) are pickled. To run the file execute the following command in a terminal:
```
python indexer.py
```
#### Step 2.a: Run boolean.py
Run this file for simple boolean queries that have AND OR and NOT operators. To do so execute the following command:
```
python boolean.py
```
A prompt will be generated to type in the input query. The number and list of documents containing the result of the given query will be printed

#### Step 2.b: Run wildcard.py
Run this file for wildcard queries. To do so execute the following command:
```
python wildcard.py
```
A prompt will be generated to type in the input query. The number and list of documents containing the result of the given query will be printed