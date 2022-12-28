#!/usr/lib/python3
import requests
import yaml

def HostLogs(workdirectory,AuthToken,tenantid,portal,starttimeUNIX,endtimeUNIX,starttimenanosec,endtimenanosec) :

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile,Loader=yaml.FullLoader) 

    payload={}
    headers = {
     'Authorization': AuthToken,
     'Content-Type': 'application/json'
    }

    valueurl = "https://"\
        +portal+\
        "/logsrql/api/v7/tenants/"\
        +tenantid+\
        "/logs/label/host/values?start"\
        +str(starttimeUNIX)+\
        "&end="\
        +str(endtimeUNIX)

    value_response = requests.request("GET", valueurl, headers=headers, data=payload)
    valuesresponsejson = value_response.json()
    valuesdata = valuesresponsejson['data']

    for i in valuesdata:

        logsurl = "https://"\
            +portal+\
            "/logsrql/api/v7/tenants/"\
            +tenantid+\
            "/logs?query={host="\
            '"'\
            +i+\
            '"'\
            "}&limit=51&start="\
            +str(starttimenanosec)+\
            "&end="\
            +str(endtimenanosec)

        log_response = requests.request("GET", logsurl, headers=headers, data=payload)
        if log_response.status_code == 200:
            logsresponsejson = log_response.json()
            logsdata = logsresponsejson['data']
            logsresultdata = logsdata['result']

            if not logsresultdata:
                status = "Host : " + i + " : Validation Fail - Logs are not coming for that host"
                parsedreportfile['Host_Logs'] = status
            else:
                status = "Host : " + i + " : Validation Pass - Logs are coming for that host"
                parsedreportfile['Host_Logs'] = status
        else :
            status = log_response.reason
            parsedreportfile['Host_Logs'] = status       
            
    with open(workdirectory + "/Report.yml","w") as file :
        yaml.dump(parsedreportfile,file)        