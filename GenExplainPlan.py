import cx_Oracle
import os
import sys


def getsqlexplainplan(sqlfile,connection):
    con = cx_Oracle.connect(connection)
    cursor = con.cursor()
    #print('Inside explain plan gen')
    sqlfilename=os.path.basename(sqlfile)
    exppath=os.path.dirname(sqlfile)
    exp_file=exppath+'\\'+sqlfilename[:-4]+'_E.SQL'
    sql='explain plan for  '
    with open(sqlfile)as myfile:
        for line in myfile:

            sql=sql + line.strip('  ')

    last_word=sql.index(';')

    #print(sql[0:last_word])

    cursor.execute(sql[0:last_word])

    cursor.execute('select * from table(dbms_xplan.display())')
    ## Maintaining the original version of sysdout
    default_stdout = sys.stdout
    file_handle = open(exp_file,'w')
    try:
        for res in cursor:
            result = res[0]
            sys.stdout = file_handle

            print(result)
    finally:
        sys.stdout = default_stdout


    con.close()


if __name__=='__main__':
    getsqlexplainplan('C:\\Users\\609700288\\desktop\\Idea\\test\\PythonGenerated\\1.SQL')