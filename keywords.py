'''
Setup: pip install rake-nltk
python -c "import nltk; nltk.download('stopwords')"
https://pypi.org/project/rake-nltk/

Output: ID + number of title keywords + title keywords + content keywords

TOTEST: line 50 min_length, max_length
line 41 score threshold
'''

import os
import sys
import csv
from rake_nltk import Rake


# simple function
def simple_rake(text):
    rakeExtract = Rake(min_length=1, max_length=4)
    rakeExtract.extract_keywords_from_text(text)
    result = rakeExtract.get_ranked_phrases_with_scores()
    top_words = []
    for (score, phrase) in result:
        top_words.append(phrase)
    return result


def writeback(content_keyword, title_keyword, newsID, writer):
    writer.writerow([newsID, len(title_keyword)] + title_keyword + content_keyword)
    return


def extract_title(rakeExtract, title):
    redundant = title.rfind('-') - 1
    title = title[:redundant]
    keywords = rake_model(rakeExtract, title, 0)
    if not keywords:
        return [title]
    return keywords

'''
return the top 10 scored phrases
if 0, then all returned without score
'''
def rake_model(rakeExtract, text, range):
    rakeExtract.extract_keywords_from_text(text)
    if range > 0:
        result = rakeExtract.get_ranked_phrases_with_scores()
        top_words = []
        for (score, phrase) in result:
            if float(score) < 10:
                break
            top_words.append(phrase)
        return top_words
    else:
        return rakeExtract.get_ranked_phrases()


def keyword(dataFilenames):
    rakeExtract = Rake(min_length=2, max_length=4)
    for filename in dataFilenames:
        keywordname = filename[:-4] + "keyword.csv"
        with open(filename, newline='', encoding="latin-1") as csvfile:
            with open(keywordname, 'w', newline='') as csvfileW:
                reader = csv.reader(csvfile, delimiter=',')
                writer = csv.writer(csvfileW)
                for row in reader:
                    content_keyword = rake_model(rakeExtract, row[9], 10)
                    title_keyword = extract_title(rakeExtract, row[2])
                    writeback(content_keyword, title_keyword, row[1], writer)
    return


def main():
    currentDir = os.path.dirname(os.path.realpath(__file__))
    dataDir = "all-the-news/"

    csv.field_size_limit(sys.maxsize)
    dataFilenames = [os.path.join(currentDir, dataDir, "articles2.csv")]
    # for filename in os.listdir(dataDir):
        # dataFilenames.append(os.path.join(currentDir, dataDir, filename))
    
    keyword(dataFilenames)


if __name__ == '__main__':
    main()
