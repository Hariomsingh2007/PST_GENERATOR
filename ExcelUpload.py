'''
Step 1: Identifying the files for which file needs to be upload will hapen

step 2: get the start position for various things from the config file


'''

import configparser
import os
import time

import TargetTableDetails

import PopulateExcel


def getfilenameforupload(folder):

    filelist=os.listdir(folder)
    ex_file_list=[]
    for files in filelist:
        if '_E.SQL' in files:
            print(files)
            ex_file_list.append(files)
    return ex_file_list

def getxldata(filename):
    #basename=os.path.basename(filename)
    #sqlfilename=expfilename.replace('_E','')
    print('Processing for file sql file -->',filename)
    #sqlfie=basename+'//'+sqlfilename
    TargetDetails= TargetTableDetails.getDMLDetails(filename)
    print('TargetDetails  -->',TargetDetails)
    return TargetDetails

def getvalidsqlfile(ex_file_list):
    sql_file_list=[]
    for l in ex_file_list:
        e=l.replace('_E', '')
        sql_file_list.append(e)
    print(sql_file_list)
    return sql_file_list

def getconfigDetails(foldername):
    # It is assumed that python will be installed in Default location c:\pythin\python35
    # config file also need to be placed in this base location as me as that of the file
    Config_Details={}
    Configuration = configparser.ConfigParser()
    try:
        Configuration.read(foldername+'\\'+'config.ini')

        tar_tab_load_cnt_st_pos=Configuration.get('excelfiledetails','Target_table_load_cnt_st_pos')
        Prod_time_Est_start_pos = Configuration.get('excelfiledetails', 'Prod_time_Estimate_start_pos')
        Att_sql_pos_start_pos = Configuration.get('excelfiledetails', 'Attach_sql_position_start_pos')
        Att_exp_plan_start_pos = Configuration.get('excelfiledetails', 'Attach_explain_plan_start_pos')
        PSTfilename=Configuration.get('excelfiledetails', 'PST_Filename')

        # start loading the configurations details # harry tum pagal hai
        Config_Details['Target_table_load_cnt_st_pos']=tar_tab_load_cnt_st_pos
        Config_Details['Prod_time_Estimate_start_pos'] = Prod_time_Est_start_pos
        Config_Details['Attach_sql_position_start_pos'] = Att_sql_pos_start_pos
        Config_Details['Attach_explain_plan_start_pos'] = Att_exp_plan_start_pos
        Config_Details['PST_Filename']=PSTfilename

        return Config_Details

    except Exception as e:
        print('Config file is not found at loaction',foldername)

def attachfile(xlfilename,total_count,command1,command2):

    statement='C:\Python35\ExcelEmbedder.exe '
    statement=statement+xlfilename+" "
    statement=statement+str(total_count)+" "
    statement=statement+command1 +" "
    statement=statement+command2

    print('Final Statment')
    print(statement)
    os.system(statement)
    time.sleep(2)
        # this is completed l

def SQLExcelupload(xlfilename,pyhthongeneratedfolder,sqlfilelist,sqlfilestartpos):


    command=''

    count=0
    s_los = int(sqlfilestartpos[1:])
    for f in sqlfilelist:
        s_los=s_los+count
        command=command+" "+sqlfilestartpos[0:1]+str(s_los)+" "+pyhthongeneratedfolder+"\\"+f
        count+=1

    return command
    # final call to exe for upload

    #del f1

def EXPExcelupload(xlfilename,pyhthongeneratedfolder,expfilelist,expfilestartpos):
    command=''
    count = 0
    s_los = int(expfilestartpos[1:])
    for f in expfilelist:
        s_los = s_los + count
        command = command + " " + expfilestartpos[0:1] + str(s_los) + " " + pyhthongeneratedfolder + "\\" + f
        count += 1
    print(command)
    # final call to exe for upload
    return command

    #del e1





def main_data_update(folderofSQLfile):
    # it always need the base location of the PST file
    folder=folderofSQLfile+'\\'+'PythonGenerated'
    try:
        file_list = getfilenameforupload(folder)
    except:
        print('System PythonGenerated folder Does not Exist')

    try:
        sqlfileslist = getvalidsqlfile(file_list)
    except:
        print('Sql files has issue inside python Generated folder')

    XlDetails = getconfigDetails(folderofSQLfile)
    count=0
    for f in sqlfileslist:
        sfile=folder + '\\' + f
        tab_details=getxldata(sfile)
        print(tab_details)
        pstfilename=XlDetails['PST_Filename']
        # tab_details {table_name,table_count,table_load_time}
        xfile=folderofSQLfile+'\\'+pstfilename
        f1= PopulateExcel.PopulateExcel(xfile)
        tab_load_pos=XlDetails['Target_table_load_cnt_st_pos']
        tab_time_pos=XlDetails['Prod_time_Estimate_start_pos']
        l_pos=int(tab_load_pos[1:])
        l_pos=l_pos+count
        t_pos=int(tab_time_pos[1:])
        t_pos=t_pos+count
        col_l_pos=tab_load_pos[0:1]+str(l_pos)
        col_t_pos=tab_time_pos[0:1]+str(t_pos)

        # cooking the column data for display
        # populating the table name and count
        str1=tab_details['table_name']+'  -->  '
        str2=tab_details['table_count']
        table_pop=str1+str2
        table_time_pop=tab_details['table_load_time']

        f1.populatedata(col_l_pos,table_pop)
        f1.populatedata(col_t_pos,table_time_pop)

        #populating the time taken
        del f1
        count+=1

def main_file_attach(folderofSQLfile):

    folder = folderofSQLfile + '\\' + 'PythonGenerated'
    try:
        file_list = getfilenameforupload(folder)
        print('filelist---->',file_list)
    except:
        print('System PythonGenerated folder Does not Exist')

    try:
        sqlfileslist = getvalidsqlfile(file_list)
    except:
        print('Sql files has issue inside python Generated folder')

    XlDetails = getconfigDetails(folderofSQLfile)
    pstfilename = XlDetails['PST_Filename']
    PST_Excel_file=folderofSQLfile+'\\'+pstfilename
    start_pos_sqlfile=XlDetails['Attach_sql_position_start_pos']
    start_pos_expfile = XlDetails['Attach_explain_plan_start_pos']

    command1=SQLExcelupload(PST_Excel_file,folder,sqlfileslist,start_pos_sqlfile)

    command2=EXPExcelupload(PST_Excel_file,folder,file_list,start_pos_expfile)
    total_count=len(sqlfileslist) +len(file_list)

    attachfile(PST_Excel_file,total_count,command1,command2)








if __name__=='__main__':
    folder='C:\\Users\\609700288\\desktop\\Idea\\test'
    #main(folder)
    main_file_attach(folder)

















