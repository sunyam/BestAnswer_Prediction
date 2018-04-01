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


def poolWork(answerIdList, questionVector, answerVector):

    def calculate_QA_sim(ans_vector, que_vector):
        simQA = cosine_similarity(ans_vector, que_vector)
        return simQA[0][0]

    def calculate_Ans_sim(main_vector, other_vector):
        simAA = cosine_similarity(main_vector, other_vector)
        return simAA[0][0]

    feat = {}
    for answerId in answerIdList:
        temp_dict = {}

        # Calculate competitor_num:
        temp_dict['competitor_num'] = len(answerIdList) - 1

        # Calculate ans_index: the order that A was created (e.g. it is the 2nd answer to the question)
        temp_dict['ans_index'] = answerIdList.index(answerId) + 1

        # Calculate QA_sim:
        answerVectorMain = answerVector[answerId]
        QA_sim = calculate_QA_sim(answerVectorMain, questionVector)
        temp_dict['QA_sim'] = QA_sim

        # Calculate ave/min/max similarity:
        similarities = []
        for vectorId in answerVector.keys():
            if vectorId != answerId:
                answerVectorOther = answerVector[vectorId]
                sim = calculate_Ans_sim(answerVectorMain, answerVectorOther)
                similarities.append(sim)
        temp_dict['min_ans_sim'] = min(similarities)
        temp_dict['max_ans_sim'] = max(similarities)
        temp_dict['ave_ans_sim'] = sum(similarities) / float(len(similarities))

        # Saves feature vector for main answer post
        feat[answerId] = temp_dict

    return feat

FEATURE_VECTOR = {}
skipList = []
errorList =[]
def poolCallback(features):
    global FEATURE_VECTOR
    for answerId in features.keys():
        try:
            FEATURE_VECTOR[answerId] = features[answerId]
        except:
            print('Answer ID %s led to an error' % str(answerId))
            print('Continuing...')


def main():
    global FEATURE_VECTOR
    global skipList
    global errorList

    pool = multiprocessing.Pool(processes=32)

    unique_question_ids = set(python_df['ParentId'].tolist())

    counter = 0
    t0 = time.time()
    for questionId in unique_question_ids:
        try:
            # Consider only the answers to the given 'questionId'
            temp_df = python_df.loc[python_df['ParentId'] == questionId]
            # Sort for the calculation of feature 'ans_index'
            temp_df.sort_values('CreationDate', inplace=True)
            # Get list of answers for that question
            answerIdList = temp_df['Id'].tolist()

            # If just one answer for the question, skip:
            if len(answerIdList) < 5:
                skipList.append(questionId)
            else:
                # Compile question vector, and its associated answer vector
                questionVector = question_vectors[questionId]
                answerVector = {}
                for answerId in answerIdList:
                    answerVector[answerId] = answer_vectors[answerId]

                pool.apply_async(poolWork,
                                 args=(answerIdList, questionVector, answerVector),
                                 callback=poolCallback)
        except Exception as e:
            print('QuestionId %s introduces an error' % str(questionId))
            print(e)
            print('Continuing...')
            errorList.append(questionId)

        # Keep track of number of questions:
        counter += 1
        if counter % 1024 == 0:
            t1 = time.time()
            print('Questions covered so far: %d in %f' % (counter, t1-t0))
            t0 = t1

        # Saves checkpoints
        if counter % 8192 == 0:
            with open('data/pickle/FEATURE_VECTOR/FV_%06d' % counter, 'wb') as f:
                cPickle.dump(FEATURE_VECTOR, f)
                FEATURE_VECTOR = {}
            with open('data/pickle/FEATURE_VECTOR/SL_%06d' % counter, 'wb') as f:
                cPickle.dump(skipList, f)
                skipList = []

    pool.close()
    pool.join()
    print('Done!')
    with open('data/pickle/FEATURE_VECTOR/ErrorList', 'wb') as f:
        cPickle.dump(errorList, f)

if __name__ == '__main__':

    # Load average question and answer vectors (calculated in average_vector.py)
    question_vectors_path = 'data/pickle/SO_Questions_vectors.pkl'
    answer_vectors_path = 'data/pickle/SO_Answers_vectors.pkl'

    print('Unpickling question vectors file...')
    with open(question_vectors_path, 'rb') as questions:
        question_vectors = cPickle.load(questions)

    print('Unpickling answer vectors file...')
    with open(answer_vectors_path, 'rb') as answers:
        answer_vectors = cPickle.load(answers)

    # Load processed_answers.csv
    print('Reading AnswersPython.csv file...')
    python_df = pd.read_csv('data/proc/AnswersPython.csv')

    print('We have %d question-vectors and %d answer-vectors.' % (len(question_vectors), len(answer_vectors)))
    main()
