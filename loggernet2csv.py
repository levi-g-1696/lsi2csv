import csv,os
import random,string,datetime
import logging
from ftplib import FTP
from tools import confreader, config, columnReader, getLinesByFolder, updateTheLastUpdateTable

from dateutil.parser import parse
logfile= r".\Log\parsing.log"
structFile= r".\stationStruct.csv"
#lastUpdateFile=r".\Log\lastUpdare.csv"
# lsiServer= "2.55.89.1"
# ftpUser= "shamat"
# ftppsw= "23enViro23"
# ftpport= 21


def makeFileName(stationName, destFolder):
    time= datetime.datetime.now()
    formatStr="fromLogntDAT-"
    zeroChar = ""
    if (time.month < 10): zeroChar = "0"

    fullFilePath = destFolder + "\\" + stationName + "." + formatStr + str(time.year) + zeroChar + str(time.month) + str(time.day) + "." + str(time.hour) + str(time.minute)
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
def cr1000ToCsv(configFile, destFolder):
    conf= confreader(configFile)
    tabTagList= conf.tabTag
    foldersList=conf.folder
    stationTypeList= conf.stationType
    logging.basicConfig(filename=logfile, level=logging.INFO, filemode = 'a',format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

    for i in range (len(tabTagList)):
      tabTag= tabTagList[i]
      tabType="asHulda"
      str1= getHeadString(stationTypeList[i])
      rawDataLines= getLinesByFolder(foldersList[i])
      if len (rawDataLines) >0:
          csvDataLines=[]
          for line in rawDataLines:
             str2 = getValString(tabTag,line)
             csvDataLines.append(str2)

          print (i, tabTag)
          destfile = makeFileName(tabTag, destFolder)
          with open(destfile, "a",newline='') as myfile:
            myfile.write(str1 + "\n")
            for line in csvDataLines:

              myfile.write(line )
              print(line)
              modifLine= line[0:35].replace(",","_") +'..'
              modifLine= modifLine.replace("\n","")
              logString=f"loggernet data line {modifLine} was succesfuly written to  {destfile}"
              print(logString)
              logging.info(","+logString+"," +tabTag)
              updateTheLastUpdateTable(tabTag)

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




#str1= getHeadString("penman")
#str2= getValString("164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,")
#line= "164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,"
#file=r"D:\import Penman\lsi\05_07_2023 16_56.lsi"
#@lsi2csv(file,r"D:\import Penman\csv")

#####################
#name= "a31"
destFolder= r"D:\import loggernet\10min"
#file= ".\\work\\Hulda10m_2023_07_26_1030.dat"
now=  datetime.datetime.now()

#cr1000ToCsv(".\\config.csv", destFolder)