''' This is class to generate the individual sql file'''

import os

import GetFileNames 


class FileGenerator:
    def __init__(self, filepath, filename, line_details):
        self.filepath = filepath
        self.filename = filename
        self.line_details=line_details
        self.fullfile=filepath+'\\'+filename

    def getnewstart(self):
        s = self.line_details[0::2]
        for item in s:
            yield item

    def getnewend(self):
        e = self.line_details[1::2]
        for item in e:
            yield item

    def gensqlfile(self):

        try:
            s = self.getnewstart()
            start = s.__next__()
            #print(start)
            e = self.getnewend()
            end = e.__next__()
            #print(end)

        except:
            print('Error while getting the list for start and end of lines in file')

        newsqlfilenumber = GetFileNames.getsqlfilename()
        os.makedirs(self.filepath+'\\PythonGenerated')
        try:
            with open(self.fullfile) as myFile:
                for num, line in enumerate(myFile, 1):
                    if num == start - 1:
                        #print('star--->', start)
                        file = self.filepath + '\\PythonGenerated\\' + str(newsqlfilenumber.__next__())
                        print('Generated File--->',file)
                        f = open(file, 'w')
                    elif num >= start and num <= end:
                        f.write(str(line))
                    elif num > end:
                        #print('reached end of line')
                        f.close()
                        try:
                            start = s.__next__()
                            #print(start)
                            end = e.__next__()
                            #print(end)
                        except:
                            pass

                    else:
                         pass

        except Exception as e :
             print(str(e))
             print('Error has Occured While FIle generation')













