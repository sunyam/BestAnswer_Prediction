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
    
    # Set this flag to be True if processing Questions.csv; False for Answers.csv:
    Q_FLAG = False

    #df_path = '../Dataset/pythonquestions/Questions.csv'
    #df_path = 'data/proc/QuestionsPythonClean.csv'
    df_path = 'data/proc/AnswersPython.csv'
    python_df = pd.read_csv(df_path)
    
    # Loading Word2Vec model:
    #path_to_model = '/Users/sunyambagga/Desktop/SO_model.word2vec'
    path_to_model = 'data/word2vec/model.word2vec'
    model = gensim.models.Word2Vec.load(path_to_model)

    # If dealing with questions:
    if Q_FLAG:
        print "Processing the Questions ...."
        python_df['NewBody'] = python_df['Title'] + python_df['Body']
        df = python_df[['Id', 'NewBody']]
        output_filename = 'SO_Questions_vectors.pkl'

    else:
        print "Processing the Answers ...."
        df = python_df[['Id', 'Body']]
        output_filename = 'SO_Answers_vectors.pkl'
    
    # Have to dropna() because 2 bodies were 'nan' in Answers.csv
    df.dropna(inplace=True)

    # Dictionary to map ID to vector:
    map_id_to_vec = {}
    
    tuples = [tuple(x) for x in df.values]
    k = 0
    for (ID, body) in tuples:
        cleanBody = unicode(body, errors='ignore')
        vec = calculate_vector(cleanBody)
        map_id_to_vec[ID] = vec
        
        # After removing nan's, should be no more floats (checking anyway)
        if type(body) == float:
            print "Why float: ", body
        
        k += 1
        if k % 10000 == 0:
            print "Done: ", k

    print "Null vector (vector of three hundred 0's) count: ", null_vector_count

    # Pickle the average-vectors for later use:
    #relative_path = '/Users/sunyambagga/Desktop/'
    relative_path = 'data/pickle/'
    with open(relative_path + output_filename, 'wb') as f:
        pickle.dump(map_id_to_vec, f)
    print "\nSuccessfully pickled " + str(len(map_id_to_vec)) + " posts."
