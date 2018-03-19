'''
   Calculating average vector for each post (answer/question), and pickling them for later use.
'''


import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import pickle
import gensim

null_vector_count = 0

def calculate_vector(body):
    global null_vector_count

    # Filter words if they are not present in our word2vec model
    my_words = []
    for w in word_tokenize(body):
        if w in model:
            my_words.append(w)

    # Average vectors of each word:
    vector = [0.0]*300
    numberOfWords = 0
    
    for w in my_words:
        numberOfWords += 1
        vec = model[w]
        vector = np.add(vector, vec)
    
    # If none of the words are in our model, return a null vector: vector of all 0s.
    if numberOfWords == 0:
        null_vector_count += 1
        return vector

    # Else, average:
    avg_vector = np.nan_to_num(vector/numberOfWords)
    return avg_vector


if __name__ == '__main__':
    
    # Loading Word2Vec model:
    path_to_model = '/Users/sunyambagga/Desktop/SO_model.word2vec'
    model = gensim.models.Word2Vec.load(path_to_model)
    
    # Pick ID and Body columns from the CSV:
    df_path = '../Dataset/pythonquestions/procPythonAnswers.csv'
    python_df = pd.read_csv(df_path)
    df = python_df[['Id', 'Body']]
    
    # Have to dropna() because 2 bodies were 'nan' in Answers.csv
    df.dropna(inplace=True)

    # Dictionary to map ID to vector:
    answers_id_vec = {}
    
    tuples = [tuple(x) for x in df.values]
    k = 0
    for (ID, body) in tuples:
        cleanBody = unicode(body, errors='ignore')
        vec = calculate_vector(cleanBody)
        answers_id_vec[ID] = vec
        
        # After removing nan's, should be no more floats (checking anyway)
        if type(body) == float:
            print "Why float: ", body
        
        k += 1
        if k % 100000 == 0:
            print "Done: ", k

    print "Null vector (vector of three hundred 0's) count: ", null_vector_count

    # Pickle the average-vectors for later use:
    with open('/Users/sunyambagga/Desktop/SO_feature_vectors.pickle', 'wb') as f:
        pickle.dump(answers_id_vec, f)
    print "\nSuccessfully pickled " + str(len(answers_id_vec)) + " posts."
