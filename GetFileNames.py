def getsqlfilename():
    names = range(1, 100)
    for n in names:
        yield str(n) + '.SQL'


def getexpfilename():
    names = range(1, 100)
    for n in names:
        yield str(n) + '_E.SQL'




