''' This is class to provide the sql lines number details from any file
@author : Hari om Singh '''


class sqldetails:
    ## file is full file name along with path
    def __init__(self, file):
        self.file = file

    def getsqldetails(self):
        sql_lines = []

        with open(self.file) as myFile:
            for num, line in enumerate(myFile, 1):
                if '----###START###' in line:
                    sql_lines.append(num + 1)
                if '----####END###' in line:
                    sql_lines.append(num - 1)

        return sql_lines






