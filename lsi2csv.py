import csv
import random,string,datetime
from dateutil.parser import parse
directory= r"C:\Users\office22\Desktop\zmani\agricultCSV"
structFile= r".\stationStruct.csv"
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


#####################################

structFile= r".\stationStruct.csv"

#str1= getHeadString("penman")
#str2= getValString("164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,")
#line= "164,05/07/2023 00:00:00,6.800000,1,7.900000,1,6.800000,1,"
file=r"C:\Users\office22\Desktop\zmani\05_07_2023 16_41.lsi"
n= lsi2csv(file,directory)
print (f"{n} csv files were created")
#####################
print ("@@@@@@    sftp section    @@@@@@@@@")
import pysftp as sftp
import os
import pysftp
from stat import S_IMODE, S_ISDIR, S_ISREG

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp=pysftp.Connection('2.55.89.1', username='shamatpen',password='23enViro23',cnopts=cnopts)



local_path=r"C:\Users\office22\Desktop\Agicult proj"

getBySFTP5Latest(sftp,  local_path, preserve_mtime=False)