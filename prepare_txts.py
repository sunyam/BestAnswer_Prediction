'''
   Writing the 'Body' (or Body+Title) of the CSV file into separate .txt files, so word2vec can process them. 
'''
import multiprocessing

import pandas as pd

def write_questions_to_txt(input_path, output_path, name):
    print(input_path)

    python_df = pd.read_csv(input_path)
    python_df['All_Body'] = python_df['Title'] + python_df['Body']
    txtPython = python_df['All_Body'].tolist()

    tenPercent = len(txtPython) / 10
    #for i, body in enumerate(txtPython[:10]):
    for i, body in enumerate(txtPython):
        if i % tenPercent == tenPercent - 1:
            print('%d%%' % (i*100/len(txtPython)))
        cleanBody = unicode(str(body), errors='ignore')
        with open(output_path+'question_'+name+'_'+str(i+1)+'.txt', 'wb') as f:
            f.write(cleanBody)


def write_answers_to_txt(input_path, output_path, name):
    print(input_path)

    python_df = pd.read_csv(input_path)
    txtPython = python_df['Body'].tolist()

    tenPercent = len(txtPython) / 10
    #for i, body in enumerate(txtPython[:10]):
    for i, body in enumerate(txtPython):
        if i % tenPercent == tenPercent-1:
            print('%d%%' % (i*100/len(txtPython)))
        cleanBody = unicode(str(body), errors='ignore')
        with open(output_path+'answer_'+name+'_'+str(i+1)+'.txt', 'wb') as f:
            f.write(cleanBody)

def write_to_txt(content):
    name, answers, questions = content
    outputPath = 'data/txt2/'
    write_answers_to_txt('data/proc/%s.csv' % answers, outputPath, name)
    write_questions_to_txt('data/proc/%s.csv' % questions, outputPath, name)

if __name__ == '__main__':
    # NOTE: If preparing txt(s) for pythonquestions, change name variable to 'python' and the paths obviously.
    # name variable is to make sure it doesn't overwrite an existing txt file.
    '''
    # 1) For answers:
    input_path = '../Dataset/stacksample/procStacksampleAnswers.csv'
    output_path = '../Dataset/TXT/'
    name = 'stack'
    write_answers_to_txt(input_path, output_path, name)

    # 2) For questions:
    inp_path = '../Dataset/stacksample/Questions.csv'
    out_path = '../Dataset/TXT/'
    name = 'stack'
    write_questions_to_txt(inp_path, out_path, name)
    '''

    filename = [
        ('python', 'AnswersPython', 'QuestionsPython'),
        ('stack', 'AnswersStack', 'QuestionsStack'),
    ]
    #pool = multiprocessing.Pool()
    #pool.map(write_to_txt, filename)
    for name in filename:
        write_to_txt(name)



