import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_vector(output_filename):
    vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words='english')

    ids = df['Id'].tolist()
    bodies = df['Body'].tolist()

    tfidf = vectorizer.fit_transform(bodies)

    map_id_to_vec = {}
    for ID, vec in zip(ids, tfidf.toarray()):
        map_id_to_vec[ID] = vec

    # Pickle it:
    with open('/Users/sunyambagga/Desktop/'+output_filename, 'wb') as f:
        pickle.dump(map_id_to_vec, f)



if __name__ == '__main__':

    # Set this flag to be True if processing Questions.csv; False for Answers.csv:
    Q_FLAG = True

    df_path = '../Dataset/pythonquestions/Questions.csv'

    python_df = pd.read_csv(df_path)

    # If dealing with questions:
    if Q_FLAG:
        print "Processing the Questions ...."
        python_df['NewBody'] = python_df['Title'] + python_df['Body']
        df = python_df[['Id', 'NewBody']]
        # Renaming the columns:
        df.columns = ['Id', 'Body']
        output_filename = 'TFIDF_Questions_vectors.pkl'

    else:
        print "Processing the Answers ...."
        df = python_df[['Id', 'Body']]
        output_filename = 'TFIDF_Answers_vectors.pkl'

    # Have to dropna() because 2 bodies were 'nan' in Answers.csv
    df.dropna(inplace=True)
    calculate_vector(output_filename)
