import csv,os
import random,string,datetime
import shutil, random
from ftplib import FTP
'''penmanLsiDir
penmanTargetDir
tabCaption="pen"  in the penmanLsi2CsvIteration()
'''
from dateutil.parser import parse

structFile= r".\stationStruct.csv"
lsiServer= "2.55.89.1"
ftpUser= "shamat"
ftppsw= "23enViro23"
ftpport= 21


def makeFileName(stationName, destFolder, datetime):
    formatStr="fromLSI-"
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
def getValString(line):
    from dateutil.parser import parse
    from datetime import datetime


    lineArr= line.split(",")
    tabName= "pen"+ lineArr[0]
    dateStr=lineArr[1]
    dt = parse(dateStr)

    dtstr= dt.isoformat()
    dtstr= dtstr.split(".")[0] #without second
    st= tabName +","+ dtstr
    for k in range(2,len(lineArr)-1,2):
       val= lineArr[k] if lineArr[k+1]=="1"  else "-99999"
       st= st+ ','+ str(val)



    return st
##################################
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
def getCsvFile(line,dir):
    str1= getHeadString("penman")

    str2 = getValString(line)

    lineArr= line.split(",")
    tabName= "pen"+ lineArr[0]
    destfile = makeFileName(tabName, dir, datetime.datetime.now())
    with open(destfile, "a") as myfile:
        myfile.write(str1 + "\n")
        myfile.write(str2 + "\n")
    print(str2)
    print(f"penman line {str2} \nwas succesfuly written to  {destfile}")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def checkLsiFormat(line):
    return all([c.isdigit() or c == ',' or c=="." or c=="/" or c==":" or c==" " or c=="\n" or c=="-"  for c in line])
##############################################
def lsi2csv(filePath,targetDir):
  with open(filePath) as f:
    lines = f.readlines()

  for line in lines:
    if not checkLsiFormat(line):
        st= set(line)
        print ("not valid character in the file:",filePath)
        print("csv files will be not created")
        print(st)
        return
  cnt=0
  for line in lines:
    getCsvFile(line,targetDir)
    cnt+=1
  return cnt
###########################################################
def getBySFTP5Latest(sftp, localdir, preserve_mtime=False):
    import warnings
    warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')

    latestfile = None
    lastFiles=[]
    for k in range(5):
      latest = 0
      for fileattr in sftp.listdir_attr():
        if  fileattr.st_mtime > latest:
            latest = fileattr.st_mtime
            latestfile = fileattr.filename



      localpath = os.path.join(localdir, latestfile)
      print("trying to download :",latestfile)
      sftp.get(latestfile, localpath, preserve_mtime=preserve_mtime)
      sftp.remove(latestfile)
   #     mode = sftp.stat(remotepath).st_mode
   #      if S_ISDIR(mode):
   #          try:
   #              os.mkdir(localpath)
   #          except OSError:
   #              pass
############################################################
def ftpDownload5Latest(ip, port, user, psw, targetDir):
    print("FTP download of 5 latest files. user:",user)
    ftp = FTP()
    try:
        ftp.connect(ip, port)
        ftp.login(user, psw)

        cnt=0

        for k in range(5):
            latest_time = None
            latest_name = None
            # get filenames within the directory
            filenames = ftp.nlst()
            if len(filenames) == 0:
                print("no files")
                return getListOfFullPath(targetDir)  # no files -exit
           # print(filenames)
            file=None
            for filename in filenames:
                local_filename = os.path.join(targetDir, filename)
                file = open(local_filename, 'wb')
                time = ftp.sendcmd("MDTM " + filename)
                if (latest_time is None) or (time > latest_time):
                    latest_name = filename
                    latest_time = time
                #     ftp.retrbinary('RETR ' + filename, file.write)
                #     ftp.delete(filename)

            ftp.retrbinary('RETR ' + latest_name, file.write)
            ftp.delete(latest_name)
            cnt +=1
          #
            print(f"File '{latest_name}' \n   (latest) is succesfully downloaded and deleted on source")

        ftp.close()

        print("ftp download session is closed")
    except  TimeoutError as ftperr:
        print("ftp error. cannot connect to bika")
    return getListOfFullPath(targetDir)
##########################################
def getListOfFullPath(directory):
    import os
    from os import listdir
    from os.path import isfile,   join

    cwd = directory
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if
                 os.path.isfile(os.path.join(cwd, f))]
    return onlyfiles

def penmanLsi2CsvIteration():
   penmanLsiDir = r"D:\import Penman\lsi"
   penmanLsiArc=r"D:\import Penman\penman lsi  arc"
   penmanTargetDir = r"D:\import Penman\csv"
   tabCaption = "pen"
   fileList= ftpDownload5Latest(lsiServer,ftpport,ftpUser,ftppsw,penmanLsiDir)
   cntLsi=0
   cntCsv=0
   print ("filelist:",fileList)
   if len (fileList) >0:
       for f in fileList:
           n= lsi2csv(f,penmanTargetDir)
           cntCsv+=n
           cntLsi+=1
           int4=random.randint(1000,9999)
           sufix=str(int4)+".lsi"
           fname= os.path.basename(f)
           shutil.move(f,penmanLsiArc+"\\"+fname +sufix)
           os.rename()

   print(f"succesfully created {cntCsv} csv files from {cntLsi} lsi")
#####################################

structFile= r".\stationStruct.csv"

#str1= getHeadString("penman")
#str2= getValString("164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,")
#line= "164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,"
#file=r"D:\import Penman\lsi\05_07_2023 16_56.lsi"
#lsi2csv(file,r"D:\import Penman\csv")
penmanLsi2CsvIteration()
#####################
