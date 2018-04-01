import cPickle
import os

def combineFV(path, getFeat=True, getSkip=False, getErro=False):

    # Get files from directory
    filenameList = os.listdir(path)

    # Ensure correctness of path
    if not path.endswith('/'):
        path = path + '/'

    featVect = {}
    skipList = []
    erroList = []

    for filename in filenameList:
        with open(path + filename, 'rb') as f:
            data = cPickle.load(f)
            if getFeat and filename.startswith('FV'):
                featVect.update(data)
            elif getSkip and filename.startswith('SL'):
                skipList.extend(data)
            elif getErro and filename.startswith('ER'):
                erroList.extend(data)

def combineDict(path):

    # Get files from directory
    filenameList = os.listdir(path)

    # Ensure correctness of path
    if not path.endswith('/'):
        path = path + '/'

    dataDict = {}

    for filename in filenameList:
        with open(path + filename, 'rb') as f:
            data = cPickle.load(f)
            dataDict.update(data)

def main():
    picklePath = 'data/pickle/FEATURE_VECTOR/'
    combineFV(picklePath, True, False, False)






if __name__ == '__main__':
    main()