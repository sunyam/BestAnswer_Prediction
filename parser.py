import lxml.html
import csv
import multiprocessing
import io


def parseFile(filename):
    with io.open('data/raw/%s.csv' % filename, 'rb') as readFile, io.open('data/proc/%s.csv' % filename, 'wb') as writeFile:
        csvReader = csv.DictReader(readFile)
        header = csvReader.fieldnames
        header.extend(['codeCount', 'urlCount', 'imgCount'])

        csvWriter = csv.DictWriter(writeFile, fieldnames=header)
        csvWriter.writeheader()

        print('Parsing %s...' % filename)
        for row in csvReader:
            # Get <code> and <a> counts (code snippets and hyperlinks)
            codeCount = row['Body'].count('<code')
            urlCount = row['Body'].count('<a')
            imgCount = row['Body'].count('<img')

            # Get last entry, i.e. Body, and strips all HTML tags
            tmp = lxml.html.fromstring(row['Body'])
            row['Body'] = tmp.text_content().encode('utf-8')

            row.update({
                'codeCount': codeCount,
                'urlCount': urlCount,
                'imgCount': imgCount,
            })

            # Write to file
            csvWriter.writerow(row)


def main():
    filename = [
        #'AnswersPython',
        #'AnswersStack',
        'QuestionsPythonClean',
        #'QuestionsStack',
    ]

    pool = multiprocessing.Pool()
    pool.map(parseFile, filename)


if __name__ == '__main__':
    main()