# Yichen Yang(yyichen)

import os
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords as sw
import csv
import sys
import collections
import pickle



def preprocess(list_filename, if_remove_stopwords, stem_type, if_lower):
    # initialize
    # stem type: 0 for not stem, 1 for porterStemmer, 2 for snowballStemmer

    # initialize tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    # initialize stopwords
    # stopwords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', \
    #                   'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', \
    #                   'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', \
    #                   'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', \
    #                   'will', 'with', 'you', 'your']
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", \
                 "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", \
                 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', \
                 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', \
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', \
                 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', \
                 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', \
                 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', \
                 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', \
                 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', \
                 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', \
                 "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', \
                 "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', \
                 "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", \
                 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", \
                 'wouldn', "wouldn't"]

    # initialize stemmer
    stemmer = None
    if stem_type == 1:
        stemmer = PorterStemmer()
    elif stem_type == 2:
        stemmer = SnowballStemmer("english")

    # read in all three files, preprocess and append to become one file
    header = []
    # all_files_without_content = []
    all_contents = []

    # word_count = {}
    # word_index = {}
    # index_word = {}

    list_filename = sorted(list_filename)
    for filename in list_filename:
        with open(filename, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader, None)
            for row in reader:
                index = int(row[0])
                if index % 100 == 0:
                    print(index)

                # if index > 300:
                #     break
                row.pop(0)
                row[0] = int(row[0])
                # row[5] = int(float(row[5]))
                # row[6] = int(float(row[6]))

                # preprocess the content
                content = row[-1]

                # add the row to all files without content
                row.pop(-1)
                # all_files_without_content.append(row)

                if if_lower:
                    readin = content.lower()
                else:
                    readin = content
                tokenized_text = tokenizer.tokenize(readin)

                # if need to remove stopwords
                if if_remove_stopwords:
                    old_tokenized_text = tokenized_text.copy()
                    tokenized_text = [word for word in old_tokenized_text if word not in stopwords]

                # if need stem
                if stem_type == 1 or stem_type == 2:
                    for i in range(len(tokenized_text)):
                        tokenized_text[i] = stemmer.stem(tokenized_text[i])

                # after preprocess, add content to contents
                all_contents.append(tokenized_text)

                # # also update the dictionary of the whole files
                # for token in tokenized_text:
                #     if token in word_count.keys():
                #         word_count[token] += 1
                #     else:
                #         word_count[token] = 1
        # break
    # print(len(word_count.keys()))

    # # store the all files:
    # with open('file_without_content.pickle', 'wb') as handle:
    #     pickle.dump(all_files_without_content, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # store the all contents file:
    with open('file_for_contents.pickle', 'wb') as handle:
        pickle.dump(all_contents, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # now fetech the first 10000 tokens
    # sorted_word_count = sorted(word_count.items(), key=lambda kv: kv[1])[::-1][0:10000]
    # print(sorted_word_count)
    # word_count = collections.OrderedDict(sorted_word_count)
    #
    # # store the first 10000 tokens
    # with open('first_10000_word.pickle', 'wb') as handle:
    #     pickle.dump(word_count, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('first_10000_word.pickle', 'rb') as handle:
    #     input_word_count = pickle.load(handle)


def re_input():
    # first read in the pickle files
    with open('first_10000_word.pickle', 'rb') as handle:
        word_count = pickle.load(handle)

    with open('file_for_contents.pickle', 'rb') as handle:
        all_contents = pickle.load(handle)

    # now use the first 10000 tokens to reindex the content
    sorted_word_count = sorted(word_count.items(), key=lambda kv: kv[1])[::-1][0:10000]

    word_index = {}
    index_word = {}

    for i in range(len(sorted_word_count)):
        pair = sorted_word_count[i]
        word_index[pair[0]] = i
        index_word[i] = pair[0]

    # store the word_index and index_word:
    with open('word_index.pickle', 'wb') as handle:
        pickle.dump(word_index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('index_word.pickle', 'wb') as handle:
        pickle.dump(index_word, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # use the word_index dictionary to update all the contents
    keys = word_index.keys()
    for i in range(len(all_contents)):
        new_content = []
        content = all_contents[i]
        for index in content:
            if index in keys:
                new_content.append(word_index[index])
        all_contents[i] = content

    with open('content_represented_by_index.pickle', 'wb') as handle:
        pickle.dump(all_contents, handle, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    csv.field_size_limit(sys.maxsize)
    dictionary_of_files = "all-the-news/"
    list_of_files = []
    for filename in os.listdir(dictionary_of_files):
        list_of_files.append(dictionary_of_files + filename)

    # list_of_file_names, if_remove_stopwords, stem_type, if use lowercase for all words
    # stem type: 0 for not stem, 1 for porterStemmer, 2 for snowballStemmer
    preprocess(list_of_files, True, 2, True)


if __name__ == '__main__':
    main()
