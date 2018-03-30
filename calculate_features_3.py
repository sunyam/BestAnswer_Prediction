'''
    Calculating the following features:
        - QuestionAnswer similarity
        - AnswerAnswer similarities
        - Number of competitor answers
        - Answer Index
'''

import cPickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import multiprocessing
import time

# Ignore stupid warnings for now:
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def calculate_QA_sim(ans_id, parent_id):
    ans_vector = answer_vectors[ans_id]
    que_vector = question_vectors[parent_id]
    simQA = cosine_similarity(ans_vector, que_vector)
    return simQA[0][0]

def calculate_Ans_sim(main_ans_id, other_ans_id):
    main_vector = answer_vectors[main_ans_id]
    other_vector = answer_vectors[other_ans_id]
    simAA = cosine_similarity(main_vector, other_vector)
    return simAA[0][0]


FEATURE_VECTOR = {}
skipList = []
def poolWork(question):
    # Consider only the answers to the given 'question'
    temp_df = python_df.loc[python_df['ParentId'] == question]
    # Sort for the calculation of feature 'ans_index'
    temp_df.sort_values('CreationDate', inplace=True)
    answer_ids = temp_df['Id'].tolist()

    # If just one answer for the question, skip:
    if len(answer_ids) == 1:
        temp_dict = {
            'competitor_num': 0,
            'ans_index': 1, 'QA_sim': 0.0,
            'min_ans_sim': 0.0,
            'max_ans_sim': 0.0,
            'ave_ans_sim': 0.0
        }
        FEATURE_VECTOR[answer_ids[0]] = temp_dict
        skipList.append(question)

    else:
        for ans_main_id in answer_ids:
            temp_dict = {}

            # Calculate competitor_num:
            temp_dict['competitor_num'] = len(answer_ids) - 1

            # Calculate ans_index: the order that A was created (e.g. it is the 2nd answer to the question)
            temp_dict['ans_index'] = answer_ids.index(ans_main_id) + 1

            # Calculate QA_sim:
            QA_sim = calculate_QA_sim(ans_main_id, question)
            temp_dict['QA_sim'] = QA_sim

            # Calculate ave/min/max similarity:
            similarities = []
            for other_id in answer_ids:
                if other_id == ans_main_id:
                    continue
                sim = calculate_Ans_sim(ans_main_id, other_id)
                similarities.append(sim)

            temp_dict['min_ans_sim'] = min(similarities)
            temp_dict['max_ans_sim'] = max(similarities)
            temp_dict['ave_ans_sim'] = sum(similarities) / float(len(similarities))

            FEATURE_VECTOR[ans_main_id] = temp_dict


def main_method():
    unique_question_ids = list(set(python_df['ParentId'].tolist()))

    pool = multiprocessing.Pool()

    counter = 0
    t0 = time.time()
    for question in unique_question_ids:
        pool.apply_async(poolWork, args=(question,))
        # Keep track of number of questions:
        counter += 1
        if counter % 32 == 0:
            t1 = time.time()
            print('Questions covered so far: %d in %d' % (counter, t1-t0))
            t0 = t1

    pool.close()
    pool.join()
    print "(kinda) Skipped questions (that had only one answer): ", len(skipList)

    # Save results
    with open(output_path, 'wb') as f:
        cPickle.dump(FEATURE_VECTOR, f)
    print "Feature vector succesfully pickled."

if __name__ == '__main__':

    # Load average question and answer vectors (calculated in average_vector.py)
    #question_vectors_path = '/Users/sunyambagga/Desktop/SO_Questions_vectors.pickle'
    #answer_vectors_path = '/Users/sunyambagga/Desktop/SO_Answers_vectors.pickle'
    question_vectors_path = 'data/pickle/SO_Questions_vectors.pkl'
    answer_vectors_path = 'data/pickle/SO_Answers_vectors.pkl'
    with open(question_vectors_path, 'rb') as questions, open(answer_vectors_path, 'rb') as answers:
        question_vectors = cPickle.load(questions)
        answer_vectors = cPickle.load(answers)
        print "We have " + str(len(question_vectors)) + " question vectors, and " + str(len(answer_vectors)) + " answer vectors."

    # Load processed_answers.csv
    #df_path = '../Dataset/proc/AnswersPython.csv'
    df_path = 'data/proc/AnswersPython.csv'
    python_df = pd.read_csv(df_path)

    #output_path = '/Users/sunyambagga/Desktop/features_2.pickle'
    output_path = 'data/pickle/features_2.pkl'
    main_method()
