###++++++++++++++++++++++++++++++++++++
import csv
import datetime
import os
import shutil
import string
import time
from collections import namedtuple
import random
lastUpdateFile=r".\Log\lastUpdate.csv"

config= namedtuple("config","enable stationName tabTag folder stationType ")


def RemoveFilesFrom(path):
    print("is removing from", path)
    for name in os.listdir(path):
        #  print ("placefile point7  ",name)

        localpath = os.path.join(path, name)
        try:
            with open(localpath, encoding='utf-8') as f:
                xxxx = 1  ## no op to close localpath
            if os.path.isfile(localpath):
                open
                os.remove(localpath)

            else:
                print("copyFileToArc: source content error")
        except PermissionError as es:
            print("CopytoArc : Pemission error")
    return


#########################
def Remove1File(localpath):
    print("system is removing :", localpath)

    try:
        with open(localpath, encoding='utf-8') as f:
            xxxx = 1  ## no op to close localpath
        if os.path.isfile(localpath):
            # open
            os.remove(localpath)

        else:
            print("copyFileToArc: source content error")
    except PermissionError as es:
        print("exception point 102030")
    return


#################     CONFREADER    ####################################
####     function read config file ####

def confreader(file):

    enable=[]




    stationName = []

    tabTag = []
    folder = []

    stationType=[]
    isEanable=0
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            isEnable=  row[0]
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif isEnable=="0" :
                line_count += 1
            else:
                enable.append (row[0])
                stationName.append(row[1])
                tabTag.append(row[2])
                folder.append(row[3])
                stationType.append(row[4])
                print("line=",line_count)
                line_count += 1

    res= config(enable,stationName,tabTag,folder,stationType)
    return res
###############################################
def columnReader(file,colname):
    colNList = []
    colnum = 0
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        colnum=0
        for row in csv_reader:
            if line_count == 0:
                cnt = 0
                for item in row:
                    if item == colname:
                        colnum = cnt
                        break
                    cnt=cnt +1
        line_count=0
        csv_file.seek(0)
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                #print (row)

                next= str(row[colnum])
                colNList.append(next)
                line_count += 1
    return colNList #returns only the column values without header
########################################################
def getLines(datFile):   # specialy for cr1000 dat files . read it and returs list of data lines only
    try:
        time.sleep(0.02)
        with open(datFile) as f:

            lines = f.readlines()
            print("getlines says:",lines[1])
            lines.pop(0)
            lines.pop(0)
            return lines
    except Exception as ex   :
        time.sleep(1.5)
        with open(datFile) as f:

            lines = f.readlines()
            print("getlines says:", lines[1])
            lines.pop(0)
            lines.pop(0)
            return lines
###################################################
def getLinesByFolder(folder)   :
  randomStr = ''.join(random.choices(string.digits + string.ascii_letters, k=5))
  arcfolder= folder+"\\newDatArc"
  dataLines=[]
  fileList= getListOfFullPath(folder)
  for f in fileList:
      lst= getLines(f)
      dataLines= dataLines +lst
      print ("extracting data from file:",f)
  arcpath = os.path.join(folder, "newDatArc")
  if not os.path.exists(arcpath):
      print ("make",arcpath)
      os.mkdir(arcpath)
  for f in fileList:
      newpath=os.path.join(arcfolder, f)
      print ("arcfolder", arcfolder, "   newpath",newpath)
      f1= f+"."+randomStr+".dat"
      shutil.move(f,f1)
      shutil.move(f1,arcpath)

  return dataLines

##########################################
def getListOfFullPath(directory):
    import os
    from os import listdir
    from os.path import isfile,   join

    cwd = directory
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if
                 os.path.isfile(os.path.join(cwd, f))]
    return onlyfiles
def writeToCsvByKey(file,keyColName,key,valColName,val):
    #here key is the first column
    import csv
    import pandas
    import pandas as pd
   # csvfile= ".\\lastUpdate.csv"
    df = pd.read_csv(file)
    rawNum= df[df[keyColName]==key].index.item()
    df.at[rawNum, valColName] = val

    print(df)
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    df.to_csv(file, index=False)
def updateTheLastUpdateTable(tab):
    file=lastUpdateFile
    keyColName = "TabTag"
    valColumnName= "LastUpdateTime"
    date_string = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'
    writeToCsvByKey(file,keyColName,tab,valColumnName,date_string)
#
# fol= "D:\pytst"
# lst= getLinesByFolder(fol)
# print (lst)
