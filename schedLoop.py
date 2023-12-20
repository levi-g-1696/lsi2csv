from datetime import datetime
import json
import os
import time
from lsi2csv import shamat24hLsiToCsvIteration
from print_color import printColor03
from tools import confreader
from loggernet2csv import cr1000ToCsv


############################################################
def getRunFlag():

    with open(initConfigFile, 'r') as f:
        json_data = json.load(f)
        if json_data["runFlag"] == 'run':
              return True
        else:return False

#############################################################
def setRunFlagON():
    with open(initConfigFile, 'r') as f:
        json_data = json.load(f)
    json_data["runFlag"] = 'run'  # On this line you needed to add ['embed'][0]
    with open(initConfigFile, 'w') as f:
        json.dump(json_data, f,indent=2)
  #######################################################
def lastRunLog():
    now =datetime.now()
    f = open(lastRunFile, "w")
    f.write("the last operation of the script was :" + str(now) + " ctime=" + str(int(now.timestamp())))
    f.close()
##################################

####################################################################################
if __name__ == '__main__':
    path= r"C:\Users\DownloadServer\PycharmProjects\lsi2csv"
    os.chdir(path)
    initConfigFile =".\\init.json"
    lastRunFile=  ".\\lastRun.log"
    config= ".\\config.csv"
    setRunFlagON()
    # bika station ftp properties
    # HOST = "2.55.125.16" #bika station
    # PORT = 19021  #
    # usr = "Loggernetsrv"
    # pwd = "23@@enviRo"
    tabTags=[]
    stNames=[]
    srcFolders=[]
    n=1000
    while getRunFlag():
        # conf= confreader(config)
        # tabTags=conf.tabTag
        # stNames = conf.stationName
        # folders= conf.folder
        #body
        with open(initConfigFile, 'r') as f:
            json_data = json.load(f)
      #  dest= json_data["destination10m"]
        dest=r"D:\import loggernet\10min"
        shamat24hLsiToCsvIteration()
        dt= datetime.now()
        printColor03(f" ####   PENMAN LSI TO CSV PARSER    ####\n")
        print    (f" ####   PENMAN LSI TO CSV PARSER    ####\n",n)

        lastRunLog()
        n=n+541
        time.sleep(5)
