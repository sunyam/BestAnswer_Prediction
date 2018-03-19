import pandas as pd

def write_to_txt(input_path, output_path):

    python_df = pd.read_csv(input_path)
    txtPython = python_df['Body'].tolist()

    for i, body in enumerate(txtPython):
        #    print body
        cleanBody = unicode(body, errors='ignore')
        with open(output_path+'python_'+str(i+1)+'.txt', 'wb') as f:
            f.write(cleanBody)

if __name__ == '__main__':
    input_path = '../Dataset/pythonquestions/procPythonAnswers.csv'
    output_path = '../Dataset/TXT/'
    write_to_txt(input_path, output_path)
