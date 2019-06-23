import  preprocess
import retrieve
import pickle
import re

def retrieve_title_date(cos_sim):
    print(cos_sim)
    index_list = [tack[0] for tack in cos_sim] 
    print(index_list)
    with open('file_without_content.pickle', 'rb') as handle:
        doc_list = pickle.load(handle)
        print(doc_list[0])
        for id in index_list:
            doc_filter = list(filter(lambda x : x[0] == id, doc_list))
            if doc_filter:
                doc = doc_filter[0] 
                info_list = [doc[0], doc[1], doc[4]] 
                print(info_list) 
    
    


def main():
    input_file = 'content_represented_by_index.pickle'
    corpus, word_index = retrieve.readPreprocessedContent(input_file)
    N = len(corpus)
    inverted_index = {}

    # can change this to return top X relevant contents based on cosine similarity score
    num_results = 10
    # can change this to tfc or bpx for query
    # can change this to tfc or nxx for document
    doc_weighting = "tfidf"
    query_weighting = "tfidf"

    retrieve.indexDocument(doc_weighting, corpus, inverted_index, word_index)

    while True:
        query = input("Please input the query:")
        query = "1 " + query
        query = re.sub("\n", " ", query)
        queryID, sorted_cos = retrieve.retrieveDocument(query, inverted_index, doc_weighting, query_weighting, N, word_index)
        chosen_cos = sorted_cos[:num_results]
        retrieve_title_date(chosen_cos)


if __name__ == "__main__":
    main()