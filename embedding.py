"""
Word embeding model used to calculate word similarity

embedding model is pretrained by glove.

the default pre-trained embedding model is:
    glove.6B.200d.txt in ./glove_embedding 

usage: 

    (1) to get word vector presentation of "man":
    
    from embedding import EmbeddingModel

    model = EmbeddingModel()
    wordVec = model.embed('man')

    (2) to get cosine similarity between words "man" and "woman":
    
    from embedding import EmbeddingModel

    model = EmbeddingModel()
    cosSim = model.similarity('man', 'woman')

    (3) To run the demo, please run:

    python3 embedding.py 

    in command line

Note: please only load the model once for multiple usages

"""
import numpy as np
import subprocess



""" 
pre-trained embedding model loaded from glove 
default model is ./glove_embedding/glove.6B.100d.txt which have 6 
billion words and 100 dimension vector presentation for each word.

To load other models, please modify the following WORD_PRESENTATION_FILE.
Other optional models are in ./glove_embedding directory

source: https://nlp.stanford.edu/projects/glove/
"""
WORD_PRESENTATION_FILE = './glove_embedding/glove.6B.200d.txt'

class EmbeddingModel:
    def __init__(self, embedding_model_file=WORD_PRESENTATION_FILE):
        self.embedding_model_file = embedding_model_file
        for i in embedding_model_file.split('.'):
            if len(i) <= 5 and 'd' in i:
                self.wordDim = int(i[:-1])
        self.wordVectors, self.vocSize = self.loadEmbedding_()


    def loadEmbedding_(self):
        """ Load embedding model from self.embedding_model_file"""
        print("Loading {}...".format(self.embedding_model_file))
        wordVectors = {}
        with open(self.embedding_model_file) as f:
            for line in f.readlines():
                line_elements = line.split()
                word = line_elements[0]
                vec = np.array([float(v) for v in line_elements[1:]])
                wordVectors[word] = vec
        return wordVectors, len(wordVectors)


    def preprocess_(self, word):
        """ Run 'ruby -n preprocess-word.rb < inpur_word' in command line """
        input_word = str.lower(word).encode('utf-8')
        cmd = ['ruby', '-n', 'preprocess-word.rb']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, input=input_word)
        out = result.stdout.decode('utf-8').strip()
        return out


    def embed(self, word):
        """ Return a vector presentation for input word"""
        preprocessed = self.preprocess_(word)
        if preprocessed not in self.wordVectors:
            print("{} is not recognized.".format(word))
            return np.zeros(self.wordDim)
        else:
            return self.wordVectors[preprocessed]

    def similarity(self, word1, word2):
        """Calculate cosine similarity for the input words: word1 and word2"""
        wordvec0 = self.embed(word1)
        wordvec1 = self.embed(word2)
        ip = np.sum(wordvec0 * wordvec1)
        norm0 = np.linalg.norm(wordvec0)
        norm1 = np.linalg.norm(wordvec1)
        if norm0 * norm1 == 0:
            cosSim = 0
        else:
            cosSim = ip/norm0/norm1 
        return cosSim


    def phraseSimilarity(self, word1, word2):
        """Calculate cosine similarity for the input words: word1 and word2"""
        words1 = word1.split()
        words2 = word2.split()
        cosSim = 0
        wordvec0 = [self.embed(word1) for word1 in words1]
        wordvec1 = [self.embed(word2) for word2 in words2]
        for vec0 in wordvec0:
            for vec1 in wordvec1:
                ip = np.sum(vec0 * vec1)
                norm0 = np.linalg.norm(vec0)
                norm1 = np.linalg.norm(vec1)
                if norm0 * norm1 == 0:
                    sim = 0
                else:
                    sim = ip/norm0/norm1 
                cosSim = np.max([sim, cosSim])
        return cosSim

if __name__ == '__main__':
    # model = EmbeddingModel()
    while True:
        option = input("- Please enter a number (1 for single word embedding,"\
                + " 2 for 2 words embedding and cos similarity, 0 for exit): ")
        if option == '0':
            break
        elif option == '1':
            word = input("- Please enter ONE word: ")
            print(word, " : ", model.embed(word))
        elif option == '2':
            words = input("- Please enter TWO word, seperate by ',': ")
            words = words.strip().split(',')
            similarity = model.phraseSimilarity(words[0], words[1])
            print("{} and {} have a cos-similarity of {}"\
                    .format(words[0], words[1], similarity))
