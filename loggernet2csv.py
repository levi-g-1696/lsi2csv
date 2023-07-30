import csv,os
import random,string,datetime
from ftplib import FTP
from tools import confreader, config, columnReader, getLinesByFolder

from dateutil.parser import parse

structFile= r".\stationStruct.csv"
# lsiServer= "2.55.89.1"
# ftpUser= "shamat"
# ftppsw= "23enViro23"
# ftpport= 21


def makeFileName(stationName, destFolder, datetime):
    formatStr="fromLogntDAT-"
    zeroChar = ""
    if (datetime.month < 10): zeroChar = "0"

    fullFilePath = destFolder + "\\" + stationName + "."+formatStr + str(datetime.year) + zeroChar + str(datetime.month) + str(datetime.day) + "." + str(datetime.hour) + str(datetime.minute)
    randomStr = ''.join(random.choices(string.digits + string.ascii_letters, k=5))
    fullFilePath = fullFilePath + "-" + randomStr + ".csv"
    return fullFilePath

##########################################
def getHeadString(tabType):
    strn= "TabularTag,DateTime"
    lst = columnReader(structFile,tabType)
    for mon in lst:
        if mon != "":
          strn = strn + "," + mon
    return strn

#############################################################
def isNumberCheck(s):
    """ Returns True if string is a number. """
    try:

        num = float(s)
        if num != num:
            return False  # NAN
        else:
            return True
    except ValueError:
        return False
    #######################################################
def getValString(tabName,line):
    from dateutil.parser import parse
    from datetime import datetime


    lineArr= line.split(",")

    dateStr=lineArr[0]
    dateStr= dateStr[1:-1]


    dt = parse(dateStr)

    dtstr= dt.isoformat()
    dtstr= dtstr.split(".")[0] #without second
    st= tabName +","+ dtstr
    for k in range(2,len(lineArr)):
       val= lineArr[k]
       if not isNumberCheck(val): val="NULL"
       st= st+ ','+ str(val)
    return st
##################################
def getCsvFiles(configFile):
    conf= confreader(configFile)
    tabTagList= conf.tabTag
    foldersList=conf.folder
    stationTypeList= conf.stationType

    for i in range (len(tabTagList)):
      tabTag= tabTagList[i]
      tabType="asHulda"
      str1= getHeadString(stationTypeList[i])
      rawDataLines= getLinesByFolder(foldersList[i])
      csvDataLines=[]
      for line in rawDataLines:
         str2 = getValString(tabTag,line)
         csvDataLines.append(str2)


      destfile = makeFileName(tabTag, dest, datetime.datetime.now())
      with open(destfile, "a") as myfile:
        myfile.write(str1 + "\n")
        for line in csvDataLines:

          myfile.write(line + "\n")
          print(line)
          print(f"loggernet data line {line} \nwas succesfuly written to  {destfile}")

#
#
def getListOfFullPath(directory):
    import os
    from os import listdir
    from os.path import isfile,   join

    cwd = directory
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if
                 os.path.isfile(os.path.join(cwd, f))]
    return onlyfiles


structFile= r".\stationStruct.csv"

#str1= getHeadString("penman")
#str2= getValString("164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,")
#line= "164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,"
#file=r"D:\import Penman\lsi\05_07_2023 16_56.lsi"
#@lsi2csv(file,r"D:\import Penman\csv")

#####################
#name= "a31"
dest= ".\\work"
#file= ".\\work\\Hulda10m_2023_07_26_1030.dat"
now=  datetime.datetime.now()

getCsvFiles(".\\config.csv")