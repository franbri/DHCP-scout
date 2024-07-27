import fileMan

if __name__ == '__main__':
    db = fileMan.loadState()
    for x in db.values():
        print(x)