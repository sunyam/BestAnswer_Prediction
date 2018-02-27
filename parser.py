import lxml.html
import csv

def main():
    with open("data/answers.csv", "rb") as readFile, open("data/procAnswers.csv", "wb") as writeFile:
        csvReader = csv.reader(readFile)
        csvWriter = csv.writer(writeFile)

        header = csvReader.next()
        header.extend(['codeCount', 'urlCount', 'imgCount'])
        csvWriter.writerow(header)

        for row in csvReader:

            # Get <code> and <a> counts (code snippets and hyperlinks)
            codeCount = row[5].count("<code>")
            urlCount = row[5].count("<a")
            imgCount = row[5].count("<img")

            # Get last entry, i.e. Body, and strips all HTML tags
            tmp = lxml.html.fromstring(row[5])
            row[5] = tmp.text_content().encode('utf-8')

            row.extend([codeCount, urlCount, imgCount])

            # Write to file
            csvWriter.writerow(row)


if __name__ == "__main__":
    main()