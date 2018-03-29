# Train a word2vec model and save it for later use

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
#import gensim
from gensim.models import Word2Vec

import os
import re
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize, sent_tokenize

# The dataset is ready (.txt files containing all StackOverflow posts, free from any useless tags)

# For more info on gensim and its usage: http://rare-technologies.com/deep-learning-with-word2vec-and-gensim/

class BlogSentences(object):
    
    def __init__(self, directory):
        # To keep a count
        self.i = 0
        
        # directory is the path to the .txt files
        self.directory = directory
    
    # Iterator for the class
    # Returns a list of words (a sentence)
    def __iter__(self):
        for txtFile in os.listdir(self.directory):
            for line in file(self.directory+'/'+txtFile, 'rb'):
                for sentence in line_to_sents(line):
                    words = sent_to_words(sentence)
                    
                    # Ignore really short sentences
                    if len(words) > 3:
                        yield words

                    if self.i % 1000 == 0:
                        print self.i
                    self.i += 1


# Converts line to sentences
def line_to_sents(line):
    sentences = sent_tokenize(line)
    for s in sentences:
        # Remove weird characters
        s = re.sub(r'[^a-zA-Z]', " ", s)
        yield s

# Converts sentences to words
def sent_to_words(sentence):
    # Make lowercase
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    my_stopwords = stopwords.words('english') + list(punctuation)
    # Filter stopwords
    words_output = []
    for w in words:
        if w not in my_stopwords:
            words_output.append(w)
    
    return words_output

pathIn = 'data/txt2'
pathOut = 'data/word2vec/model.word2vec'
#path = '/Users/sunyambagga/Desktop/SE 762/Project/Dataset/TXT'
s = BlogSentences(pathIn)
model = Word2Vec(s, size=300, workers=8, min_count=10)
#model = gensim.models.Word2Vec(s, size=300, workers=8, min_count=10)
#model.save('/Users/sunyambagga/Desktop/SO_model.word2vec')
model.save(pathOut)
