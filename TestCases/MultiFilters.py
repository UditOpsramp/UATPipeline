#!/usr/lib/python3
import requests
import yaml

def MultiFilter(workdirectory,AuthToken,tenantid,portal,starttimenanosec,endtimenanosec) :

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile,Loader=yaml.FullLoader) 

    payload={}
    headers = {
     'Authorization': AuthToken,
     'Content-Type': 'application/json'
    }
            
    logsurl = "https://"\
                +portal+\
                "/logsrql/api/v7/tenants/"\
                +tenantid+\
                '/logs?query={app="agent",type="log",file_path="/var/log/opsramp/agent.log",level="Info"}&limit=51&start='\
                +str(starttimenanosec)+\
                "&end="\
                +str(endtimenanosec)

    log_response = requests.request("GET", logsurl, headers=headers, data=payload)
    if log_response.status_code == 200:
        logsresponsejson = log_response.json()
        logsdata = logsresponsejson['data']
        logsresultdata = logsdata['result'] 
        if not logsresultdata:
            status = "Validation Fail -  MultiFilter Functionality is not Working Properly"
            parsedreportfile['MultiFilter_Functionalty'] = status 
        else:
            status = "Validation Pass - MultiFilter Functionality is  Working Properly"
            parsedreportfile['MultiFilter_Functionalty'] = status 
            
    else:
        status = log_response.reason
        parsedreportfile['MultiFilter_Functionalty'] = status    
        
    with open(workdirectory + "/Report.yml","w") as file :
        yaml.dump(parsedreportfile,file)
