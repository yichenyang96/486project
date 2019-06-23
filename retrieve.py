# Guyi (Michelle) Chen chenguy

"""
Retrieve relevant news content based on query.



usage:

    (1) Please have index_word and content_represented_by_index.pickle in the root folder

    (2) The default weighting scheme is tfidf for both query and document

    (3) The weighting scheme can change to tfc and nxx for query and nfx and bpx for document

    (4) num_results determines hwo many relevant files are retrieved. -1 means retrieve all files
    commented at line 271

    (5) The output file is called news.docscheme.queryscheme.output
    queryid docid similarity_score

    (2) To run the demo, please run:

    python3 retrieve.py

    in command line

"""

import pickle
import math
import operator
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords as sw
from nltk.tokenize import RegexpTokenizer

# read preprocessed files
def readPreprocessedContent(input_file):
    with open(input_file, 'rb') as handle:
        corpus = pickle.load(handle)

    with open('index_word.pickle', 'rb') as handle:
        word_index = pickle.load(handle)

    return corpus, word_index

# create inverted index for the corpus
def indexDocument(weighting_documents, corpus, inverted_index, word_index):

    DocID = 0
    for document in corpus:
        freq_dict = {}
        if weighting_documents == "tfidf":
            freq_dict = tfIdfFreq(document, word_index, True)
            # print(inverted_index)

        elif weighting_documents == "tfc":
            freq_dict = tfcFreq(document, word_index, True)

        elif weighting_documents == "nxx":
            freq_dict = nfxFreq(document, word_index, True)

        for word in freq_dict:
            if word not in inverted_index:
                inverted_index[word] = []
                inverted_index[word].append(1)
                inverted_index[word].append({})
                inverted_index[word][1][DocID] = freq_dict[word]
            else:
                inverted_index[word][0] += 1
                inverted_index[word][1][DocID] = freq_dict[word]

        DocID += 1

"""
   {term1: normalized_tf, term2: 0.324, ....}
"""
def tfIdfFreq(document, word_index,isContent):
    freq_dict = {}
    max_freq = 0
    for word in document:
        if isContent:
            word = word_index[word]
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
        if freq_dict[word] > max_freq:
            max_freq = freq_dict[word]
    for item in freq_dict:
        freq_dict[item] = freq_dict[item] / max_freq

    return freq_dict


def tfcFreq(document, word_index, isContent):
    freq_dict = {}
    for word in document:
        if isContent:
            word = word_index[word]
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict


def nfxFreq(document, word_index, isContent):
    freq_dict = {}
    max_freq = 0
    for word in document:
        if isContent:
            word = word_index[word]
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
        if freq_dict[word] > max_freq:
            max_freq = freq_dict[word]
    for item in freq_dict:
        freq_dict[item] = 0.5 + 0.5 * freq_dict[item] / max_freq
    return freq_dict


def tfIdfIndex(inverted_index, document_set, N):
    weighted_matrix = {}
    for token in inverted_index:
        for docID in document_set:
            if docID in inverted_index[token][1]:
                if docID not in weighted_matrix:
                    weighted_matrix[docID] = {}
                tf = inverted_index[token][1][docID]
                idf = math.log10(N / inverted_index[token][0])
                weighted_matrix[docID][token] = tf * idf
    return weighted_matrix

# calculate tfc index
def tfcIndex(inverted_index, document_set, N):
    weighted_matrix = {}
    total_weight = {}
    for token in inverted_index:
        for docID in document_set:
            if docID in inverted_index[token][1]:
                if docID not in weighted_matrix:
                    weighted_matrix[docID] = {}
                    total_weight[docID] = 0
                tf = inverted_index[token][1][docID]
                idf = math.log10(N / inverted_index[token][0])
                weighted_matrix[docID][token] = tf * idf
                total_weight[docID] += tf * idf * tf * idf

    for doc in weighted_matrix:
        for item in weighted_matrix[doc]:
            weighted_matrix[doc][item] = weighted_matrix[doc][item] / total_weight[doc]
    return weighted_matrix

# calculate nfx index
def nfxIndex(inverted_index, document_set):
    weighted_matrix = {}
    for token in inverted_index:
        for docID in document_set:
            if docID in inverted_index[token][1]:
                if docID not in weighted_matrix:
                    weighted_matrix[docID] = {}
                weighted_matrix[docID][token] = inverted_index[token][1][docID]
    # print(weighted_matrix)
    return weighted_matrix

# calculate the cosine similarity between query and document
def cosSim(doc, query):
    # calculate the dot product
    dot_product = 0
    for token in query:
        if token in doc:
            dot_product += query[token] * doc[token]
    # calculate the doc length
    doc_length = 0
    query_length = 0
    for token in doc:
        doc_length += doc[token] * doc[token]
    # calculate the query length
    for token in query:
        query_length += query[token] * query[token]

    return dot_product / math.sqrt(doc_length * query_length)


def retrieveDocument(query, inverted_index, weighting_documents, weighting_query, N, word_index):
    # preprocessing query
    queryID = query.split()[0]
    tokenizer = RegexpTokenizer(r'\w+')
    query = tokenizer.tokenize(query)
    stop_words = set(sw.words('english'))
    query = [w for w in query if not w in stop_words]
    processed_query = []
    for word in query:
         processed_query.append(PorterStemmer().stem(word))

    print("Query now")
    print(query)

    # find the set of documents that contains at least one word from the query
    document_set = []
    for word in query:
        if word in inverted_index:
            document_dict = inverted_index[word][1]
            for docID in document_dict:
                document_set.append(docID)

    # calculate query term weighting
    weighted_query = {}
    if weighting_query == "tfidf":
        freq_dict = tfIdfFreq(query, word_index, False)
        for token in freq_dict:
            if token in inverted_index:
                tf = freq_dict[token]
                idf = math.log10(N / inverted_index[token][0])
                weighted_query[token] = tf * idf
            else:
                weighted_query[token] = 0
    elif weighting_query == "nfx":
        freq_dict = nfxFreq(query, word_index, False)
        for token in freq_dict:
            if token in inverted_index:
                tf = freq_dict[token]
                idf = math.log10(N / inverted_index[token][0])
                weighted_query[token] = tf * idf
            else:
                weighted_query[token] = 0
    elif weighting_query == "bpx":
        for token in query:
            if token in inverted_index:
                df = inverted_index[token][0]
                weighted_query[token] = math.log10((N - df) / df)
            else:
                weighted_query[token] = 0

    weighted_document = {}
    if weighting_documents == "tfidf":
        weighted_document = tfIdfIndex(inverted_index, document_set, N)

    elif weighting_documents == "tfc":
        weighted_document = tfcIndex(inverted_index, document_set, N)

    elif weighting_documents == "nxx":
        weighted_document = nfxIndex(inverted_index, document_set)

    # print(weighted_query)
    # print(weighted_document)
    # calculate cosine similarity
    cos_sim_dicts = {}
    for docID in weighted_document:
        cos_sim_dicts[docID] = cosSim(weighted_document[docID], weighted_query)

    sorted_cos = sorted(cos_sim_dicts.items(), key=operator.itemgetter(1), reverse=True)
    # print(queryID)
    # print(sorted_cos)
    return queryID, sorted_cos

def writeOutput(queryID, sorted_cos, document_weight, query_weight, num_results):
    out_file_name = "news." + document_weight + "." + query_weight + ".output"

    with open(out_file_name, "a+") as out_file:
        if num_results == -1:
            for doc in sorted_cos:
                out_file.write(queryID + " " + str(doc[0]) + " " + str(doc[1]) + "\n")
        else:
            for i in range(num_results):
                out_file.write(queryID + " " + str(sorted_cos[i][0]) + " " + str(sorted_cos[i][1]) + "\n")

def prepareDocment():
    input_file = 'content_represented_by_index.pickle'
    corpus, word_index = readPreprocessedContent(input_file)
    N = len(corpus)
    inverted_index = {}

    doc_weighting = "tfidf"
    query_weighting = "tfidf"

    indexDocument(doc_weighting, corpus, inverted_index, word_index)

    return inverted_index


def main():

    input_file = 'content_represented_by_index.pickle'
    corpus, word_index = readPreprocessedContent(input_file)
    N = len(corpus)
    inverted_index = {}

    # can change this to return top X relevant contents based on cosine similarity score
    num_results = 10
    # can change this to tfc or bpx for query
    # can change this to tfc or nxx for document
    doc_weighting = "tfidf"
    query_weighting = "tfidf"

    indexDocument(doc_weighting, corpus, inverted_index, word_index)
    print("Index Document Completed!")
    with open("queries") as f:
        queries = f.readlines()
        for query in queries:
            query = re.sub("\n", " ", query)
            queryID, sorted_cos = retrieveDocument(query, inverted_index, doc_weighting, query_weighting, N, word_index)
            writeOutput(queryID, sorted_cos, doc_weighting, query_weighting, num_results)

if __name__ == '__main__':
    main()