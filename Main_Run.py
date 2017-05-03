''' This is the sampe test file to test file is generated for any file
@Author: Hari om Singh
Date   : 14-02-2017
Email  :,hariomsingh2007@gmail.com 
'''

import SqlDetails
import SqlFileGenerator
import os
import SqlTimingDetails
import GenExplainPlan
import shutil
import sys
import time
import ExcelUpload as EU
import GetConnectionDetails as Connect
import configparser






def sql_exp_generation(fullfile):
    filepath=os.path.dirname(fullfile)
    filename=os.path.basename(fullfile)
    try:
        Configuration = configparser.ConfigParser()
        Configuration.read(filepath + '\\' + 'config.ini')
        sql_timeout_time = Configuration.get('QueryTimeOutDetails', 'sql_time_out_time')
    except:
        print('Error while retriving the config.ini File')
        return False
    line_details=SqlDetails.sqldetails(fullfile)
    start_end=line_details.getsqldetails()
    #print(start_end)
    if len(start_end)%2!=0:
        raise Exception("Start and End Pattern is not Proper")
    # Self made file pattern

    Gen_path = filepath + '\\PythonGenerated'
    if os.path.isdir(Gen_path):
        shutil.rmtree(Gen_path)
    gen=SqlFileGenerator.FileGenerator(filepath,filename,start_end)
    gen.gensqlfile()

# PythonGenerated path would

    allFiles = os.listdir(Gen_path)
    print(allFiles)
    con=Connect.getconnection(filepath)
    if not Connect.testconnection(con):
        return False

    for files in allFiles:
        print('Starting getting timing Details for ',files)
        if SqlTimingDetails.GetTiming_run(Gen_path+'\\'+files,con,sql_timeout_time):
            print('Starting Generating Explain plan for  ',files)
            GenExplainPlan.getsqlexplainplan(Gen_path+'\\'+files,con)
            print('Explain Plan is Generated')

    print('Going to Start Excel Upload with Data')

# main need the sqlfilelocaton rest all is derived by own


def main(fullfile):

    sql_exp_generation(fullfile)

    #print('Error while file generation')

    folder = os.path.dirname(fullfile)

    try:
        EU.main_data_update(folder)
    except:
        print('Error While upadating Data intp PST excel Sheet')

    try:

        EU.main_file_attach(folder)
    except:
        print('Error while uploading files in PST Excel')

if __name__=="__main__":
    file_details=sys.argv[1]
    print(file_details)
    file = 'C:\\Users\\609700288\\desktop\\Idea\\test\\PKG_OM_CUST_PHASE_TEL_LOAD_DO.sql'
    main(file_details)



# status of p2-->  0 error



