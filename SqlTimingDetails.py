import cx_Oracle
import sys
import os
import multiprocessing
import time

ret = {'Gettimingdetails_status': False}

def timecount(mins):
    start=time.time()
    while(1):
        print('Time crossed in Mins -->',int((time.time()-start)/60))
        time.sleep(10)
        if int((time.time()-start)/60) > mins:

            break


def Gettimingdetails(filename,connection,queue):

    con = cx_Oracle.connect(connection)
    cursor = con.cursor()

    def DbmsOutputGetLine(cursor):
        """
        Retrieving dbms_output result line by line
        with dbms_output.get_line method.
        """
        line = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        dbms_out = []
        while True:
            cursor.callproc("dbms_output.get_line", (line, status))
            if status.getvalue() != 0:
                break
            else:
                a = line.getvalue()
                dbms_out.append(a)
        return dbms_out

    sql_middle=' '
    sql_header='''Declare
                  start_time number;
                  end_time number;
                  begin
                  start_time := dbms_utility.get_time;
                  '''
    sql_trailer='''
                  end_time := dbms_utility.get_time;
                  dbms_output.put_line(round((end_time-start_time)/100, 2 ));
                  dbms_output.put_line(sql%rowcount);
                  end;
                  '''
    with open(filename)as myfile:
        for line in myfile:
            sql_middle=sql_middle + line

    #print('sql_middle--->',sql_middle)
    sql=sql_header+sql_middle+sql_trailer
    #print('start of main sql-->',sql)


    try:
        cursor.callproc("dbms_output.enable")
        cursor.execute(sql)
        output=DbmsOutputGetLine(cursor)
    except Exception as e:
        dirname=os.path.dirname(filename)
        f_name=os.path.basename(filename)
        error_file=dirname+"\\"+f_name[:-4]+"_ERROR_LOG.SQL"
        e_file=open(error_file,'w')
        e_file.write(str(e))
        print(e)
        e_file.close()
        con.close()
        ret = queue.get()
        ret['Gettimingdetails_status'] = False
        queue.put(ret)
        return False
    else:
        f = open(filename, 'a')
        f.write('\n')
        f.write('\n ')
        time_taken='Time Taken -->'+ output[0] +' Seconds '
        f.write(time_taken)
        f.write('\n')
        rows_count='Rows Effected -->'+ output[1]
        f.write(rows_count)
        f.close()
        con.close()
        ret = queue.get()
        ret['Gettimingdetails_status'] = True
        queue.put(ret)
        return True
    #con.commit()
    con.close()

    #print('gettiming is completed')

def GetTiming_run(filename,connection_details,sql_timeout_time):
    queue = multiprocessing.Queue()
    queue.put(ret)
    p1 = multiprocessing.Process(target=timecount, args=(sql_timeout_time,))
    p2 = multiprocessing.Process(target=Gettimingdetails, args=(filename,connection_details,queue))


    p1.start()
    p2.start()
    while (1):
        # print('p1--->',p1.is_alive())
        # print('p2---->',p2.is_alive())

        if not (p1.is_alive() and p2.is_alive()):
            last_status=queue.get()
            print('Gettimingdetails_status--->',last_status,type(last_status))
            p1.terminate()
            p2.terminate()
            if last_status['Gettimingdetails_status']:
                return True
            else:
                return False


if __name__=='__main__':
    GetTiming_run('C:\\Users\\609700288\\desktop\\Idea\\test\\PythonGenerated\\2.SQL','username/password@server:port/instance')

