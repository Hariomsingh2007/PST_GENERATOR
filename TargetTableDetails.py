'''This is method to return the table name and record count'''

def gettablename(file):
    sql_element=[]
    sql_element_upper=[]
    with open(file) as f_in:
        for l in f_in:
            element = list(e for e in l.strip(' ').split() if e)
            sql_element.extend(element)
            #print(sql_element)

        sql_element_upper=list(map(str.upper,sql_element))
        #print('upper')
        #print(sql_element_upper)


        if sql_element_upper[0]=="INSERT":
            print('DML Operation:INSERT')
            ind=sql_element_upper.index('INTO')
            tablename=sql_element_upper[ind+1]
            print('table NAme-->',tablename)

        elif sql_element_upper[0]=="MERGE":
            print('DML Operation:MERGE')
            ind = sql_element_upper.index('INTO')
            tablename = sql_element_upper[ind + 1]
            print('table NAme-->', tablename)

        elif sql_element_upper[0]=="UPDATE":
            print('DML Operation:UPDATE')
            tablename=sql_element_upper[1]
            print('table NAme-->', tablename)


        elif sql_element_upper[0]=="DELETE":
            print('DML Operation:DELETE')
            tablename = sql_element_upper[1]
            print('table NAme-->', tablename)
        else:
            tablename=None
            print('Unknow DML')
    return tablename


def getdmltime(file):
    myfile=open(file,'r')
    contents = [x.strip() for x in myfile.readlines()]
    print(contents)
    time=contents[-2]
    print(time)
    return time[14:]

def getrecordcount(file):
    myfile = open(file, 'r')
    contents = [x.strip() for x in myfile.readlines()]
    count = contents[-1]
    print(count)
    return count[17:]

def getDMLDetails(file):
    tab_details={}
    tab_name=gettablename(file)
    tab_count=getrecordcount(file)
    tab_load_time=getdmltime(file)
    tab_details['table_name']=tab_name
    tab_details['table_count'] = tab_count
    tab_details['table_load_time'] = tab_load_time

    return tab_details



if __name__=='__main__':
    filename='C:\\Users\\609700288\\desktop\\Idea\\test\\PythonGenerated\\2.SQL'
    gettablename(filename)
    print(getrecordcount(filename))
    print(getdmltime(filename))




