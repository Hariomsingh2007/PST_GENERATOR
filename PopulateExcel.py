#import Exceltest.py
#import TargetTableDetails
import os
import openpyxl
import time

class PopulateExcel:

    def __init__(self,xlfilename):
        self.xlfilename=xlfilename


    def populatedata(self,column,data):
        self.column=column
        self.data=data
        xlfile = openpyxl.load_workbook(self.xlfilename)
        sheet = xlfile.get_sheet_by_name('PST')
        sheet[column] = data
        xlfile.save(self.xlfilename)

    def attachfile(self,command):

        # default location of Excelembbeder.exe is in c:\python\35

        self.command=command
        statement='C:\Python35\ExcelEmbedder.exe '
        statement=statement+self.command
        print('Final Statment')
        print(statement)
        os.system(statement)
        time.sleep(5)
        # this is completed later













