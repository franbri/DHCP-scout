import pickle,os
from pathlib import Path

if os.name == 'nt':
    tmpDir = '.\\'
elif os.name == 'posix':
    try:
        tmpDir = os.environ['TMPDIR']
    except:
        try:
            Path('/dev/shm/test').touch()
            tmpDir = '/dev/shm/'
        except:
            tmpDir = '/tmp/'

def saveState(known_hosts):
    stateFile = open(tmpDir + 'DHCP-scout.pickle', 'ab')
    pickle.dump(known_hosts, stateFile)
    stateFile.close()

def loadState():
    stateFile = open(tmpDir + 'DHCP-scout.pickle', 'rb')
    return pickle.load(stateFile)

if __name__ == '__main__':
    db = loadState()
    print(db)