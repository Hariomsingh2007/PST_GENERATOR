import configparser
import os.path
import cx_Oracle


# completing the connections string
def getconnection(foldername):
    Configuration = configparser.ConfigParser()
    print(Configuration)
    cfgfile=foldername + '\\' + 'config.ini'
    print(cfgfile)
    Configuration.read(cfgfile)
    v_username=Configuration.get('userDetails','username')
    v_host = Configuration.get('userDetails', 'host')
    v_port = Configuration.get('userDetails', 'port')
    v_sid = Configuration.get('userDetails', 'SID')
    v_password_cache =Configuration.get('userDetails', 'password_cache')
    v_pasword_key = Configuration.get('userDetails', 'pasword_key')
    password = str(input('Enter the password:'))

    '''if v_password_cache=='Y' and os.path.exists('C:\\Python35\\Lib\\excrypted.txt'):
        f=open('C:\\Python35\\Lib\\excrypted.txt')
        text=f.readlines()
        f.close()
        password=FileEncryption.decrypt(v_pasword_key,text[0])
        print('password-->',password)
    else:
        print('Please Enter your Oracle DB Password:')
        password=str(input())
        f = open('C:\\Python35\\Lib\\excrypted.txt','w')
        file_password=FileEncryption.encrypt(v_pasword_key, password)
        f.write(file_password)
        f.close()
    '''

    conn_string=v_username+'/'+password+'@'+v_host+':'+v_port+'/'+v_sid
    print(conn_string)
    return conn_string

def testconnection(conn):
    con = cx_Oracle.connect(conn)
    cursor = con.cursor()
    try:
        cur=cursor.execute('select 1 from dual')
        for res in cur:
            print('Connection Passed')
        con.close()
        return True
    except:
        print('Connection test has been failed Please check username and password')
        con.close()
        return False

if __name__=='__main__':
    c=getconnection('C:\\Users\\609700288\\desktop\\Idea\\test')
    print(testconnection(c))






