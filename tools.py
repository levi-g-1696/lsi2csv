###++++++++++++++++++++++++++++++++++++
import csv
import os
import time
from collections import namedtuple
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
def getLines(datFile):
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
  dataLines=[]
  fileList= getListOfFullPath(folder)
  for f in fileList:
      lst= getLines(f)
      dataLines= dataLines +lst
      print ("extracting data from file:",f)

  for f in fileList:
      # move f to arc
      pass
      #move f to arc
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
