import csv
import cPickle
import datetime

# Extract intra-individual features
def extractFeatures(filename):
    answers, questions = filename

    def compileUserScores(answers):
        scoreDict = {}
        with open('data/proc/%s.csv' % answers, 'rb') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                userId = row['OwnerUserId']
                score = int(row['Score'])
                scoreDict.update({
                    userId: scoreDict.get(userId, 0) + score
                })
        return scoreDict

    def compileQuestionData(questions, answers):
        questionDict = {}

        # For each question, get the number of answers
        with open('data/proc/%s.csv' % answers, 'rb') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                questionId = row['ParentId']
                questionDict.update({
                    questionId: {
                        'competitor_num': questionDict.get(questionId, {}).get('competitor_num', 0) + 1,
                    }
                })

        # For each question, get the creation date
        with open('data/proc/%s.csv' % questions, 'rb') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                questionId = row['Id']
                question = questionDict.get(questionId)
                if question is None:
                    continue
                else:
                    question.update({
                        'CreationDate': row['CreationDate']
                    })
                questionDict.update({
                    questionId: question
                })

        return questionDict

    print('Extracting features...')
    print('1. Compile user data')
    scoreDict = compileUserScores(answers)

    print('2. Compile question data')
    questionDict = compileQuestionData(questions, answers)

    print('3. Compute features')
    dataPoints = {}
    with open('data/proc/%s.csv' % answers, 'rb') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:

            try:

                questionId = row['ParentId']

                # Feature 3
                url_tag = row['urlCount']

                # Feature 4
                pic = row['imgCount']

                # Feature 5
                code = row['codeCount']

                # Feature 6
                body = row['Body']
                ans_len_char = len(body)
                ans_len_word = len(body.split())

                # Feature 7
                paragraphs = body.split('\n')
                L = []
                sumL = 0
                M = 0
                for p in paragraphs:
                    paraLength = len(p)
                    if paraLength > 0:
                        L.append(paraLength) # Length of ith paragraph
                        sumL += paraLength
                    else:
                        M -= 1
                M += len(paragraphs) # Number of paragraphs
                try:
                    L.sort()
                    maxL = L.pop()
                except:
                    maxL = 0
                readability1 = maxL # Length of longest paragraph
                readability2 = float(sumL+1)/float(M+1) # Average length per paragraph

                # Feature 8
                userId = row['OwnerUserId']
                reputation = scoreDict.get(userId, 0)

                # Feature 10
                FMT = '%Y-%m-%dT%H:%M:%SZ'
                questionTime = datetime.datetime.strptime(questionDict[questionId]['CreationDate'], FMT)
                answerTime = datetime.datetime.strptime(row['CreationDate'], FMT)
                timeSlot = (answerTime - questionTime).seconds

                # Feature 14
                competitor_num = questionDict[questionId]['competitor_num'] - 1

                point = {
                    'url_tag': url_tag,
                    'pic': pic,
                    'code': code,
                    'ans_len': ans_len_char,
                    'readability1': readability1,
                    'readability2': readability2,
                    'owner_score': reputation,
                    'timeSlot': timeSlot,
                    'competitor_num': competitor_num,
                }
                dataPoints.update({
                    row['Id']: point,
                })

            except Exception as e:
                print(e)

    print('Writing data points in file (pickle)')
    with open('data/pickle/features_%s.pkl' % answers, 'wb') as pklFile:
        cPickle.dump(dataPoints, pklFile, cPickle.HIGHEST_PROTOCOL)



def main():
    filename = [('AnswersPython', 'QuestionsPython'), ('AnswersStack', 'QuestionsStack')]
    for name in filename:
        print('Analyzing %s and %s...' % (name[0], name[1]))
        extractFeatures(name)
        print('')

if __name__ == '__main__':
    main()