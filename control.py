import json

stationsFile=".\\work\\camStations.json"
s=[]
class CampbellStation:
    stations= []
    def __init__(self,name,tab,folder,type):
        self.name= name
        self.tab= tab
        self.folder= folder
        self.type= type

       # print ("stations:",CampbellStation.stations )

    @staticmethod
    def append2list(st):
       # CampbellStation.stations.append(st)
       s.append(st)
    def append2json(self):
        with open(stationsFile, "a") as file:
            json.dump([ob.__dict__ for ob in CampbellStation.stations], file)
    @staticmethod
    def getList():
       return CampbellStation.stations

    @staticmethod
    def getStationByTab(tabName):
        for st in CampbellStation.stations:
           if st.tab == tabName :return st
        return CampbellStation ("empty","empty","empty","empty")
    @staticmethod
    def loadStationsFromFile(file):
        with open(file, 'r') as data_file:
            json_data = data_file.read()

        stList = json.loads(json_data)
        return stList

    @staticmethod
    def create_json(lst):
        with open(stationsFile, "a") as file:
            json.dump([ob.__dict__ for ob in lst], file)

def json_to_dict(obj):
    d=dict()
    d["name"] = obj.name
    d["tab"]= obj.tab
    return d
def prompt():
    print(" #####   new station input    ####")
    stName= input("station name:\n>")
    tabName=  input ("table name (for instance- a23) :\n>")
    folder= input ("source files folder:\n>")
    stType=input ("enter station type (for instance asHulda) :\n")
    new= CampbellStation(stName,tabName,folder,stType)
    d1= json_to_dict(new)
    print (d1)


    print ("afterappend: ",CampbellStation.stations)
    return d1

l= CampbellStation.loadStationsFromFile(stationsFile)
print (l)
#
new=prompt()
l= CampbellStation.loadStationsFromFile(stationsFile)
l.append(new)


print (l)
