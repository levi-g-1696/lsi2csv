from lsi2csv import columnReader, structFile


def get_val_string_for_shamat(line):
    from dateutil.parser import parse
    from datetime import datetime


    line_arr= line.split(",")
    tab_name= "ims"+ line_arr[0]
    dateStr=line_arr[1]
    dateStr= dateStr.replace("24:00","23:50")
    dt = parse(dateStr,dayfirst =True)

    dtstr= dt.isoformat()
    dtstr1= dtstr.split(".")[0] #without second

    st= tab_name +","+ dtstr1
    tab_type= tab_name
    mon_list = columnReader(structFile, tab_type)
    i =0
    for k in range(2,len(line_arr)-1,2):
       if "disabled" not in mon_list[i].lower():

         val= line_arr[k] if line_arr[k+1]=="1"  else "-99999"
         st= st+ ','+ str(val)
       i= i+1
  #  print(f"getValString says: dt={dt}, dtstr={dtstr}", dtstr1,f"   st={st}")
    return st