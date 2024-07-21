import pickle,os
from pathlib import Path

if os.name == 'nt':
    tmpDir = '.\\'
elif os.name == 'posix':
    tmpDir = os.environ['TMPDIR']
    if len(tmpDir) < 1:
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
    # initializing data to be stored in db
    Omkar = {'key' : 'Omkar', 'name' : 'Omkar Pathak', 
    'age' : 21, 'pay' : 40000}
    Jagdish = {'key' : 'Jagdish', 'name' : 'Jagdish Pathak',
    'age' : 50, 'pay' : 50000}
    
    # database
    db = {}
    db['Omkar'] = Omkar
    db['Jagdish'] = Jagdish

    saveState(db)
    print(db)