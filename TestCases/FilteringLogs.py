#!/usr/lib/python3
import requests
import yaml
import ruamel.yaml
import time
import json
import subprocess as sp

def FilteringLogs(workdirectory,AuthToken, tenantid, portal, starttimenanosec, endtimenanosec, parsedconfigfile):

    with open(workdirectory + "/TestCasesConfig/log-filerting.yaml","r") as file :
        filteringconfigfile = yaml.load_all(file,Loader=yaml.FullLoader)
        filteringconfigfilelist= list(filteringconfigfile)
    
    for i in filteringconfigfilelist:
        for k,j in i['inputs'].items():
            (j['include'][0]) = workdirectory + "/*.log" 
            
    logconfigfile = yaml.safe_dump_all(filteringconfigfilelist,sort_keys=False, explicit_start=True)
    
    yaml_new = ruamel.yaml.YAML(typ='safe')
    data = yaml_new.load(logconfigfile)          
    
    with open(workdirectory + "/TestCasesConfig/log-filerting.yaml","w") as file :
        yaml.dump(data, file,explicit_start=True,sort_keys=False)
    
    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    NumberofLogs = parsedconfigfile['NumberofLogs']
    NumberofLogFiles = parsedconfigfile['NumberofLogFiles']
    LogMsgLength = parsedconfigfile['LogMsgLength']
    LogRotateSizeInMB = parsedconfigfile['LogRotateSizeInMB']
    TimeToSleep = parsedconfigfile['TimeToSleep']

    cmd = "sudo cp " + workdirectory + "/TestCasesConfig/log-filerting.yaml /opt/opsramp/agent/conf/log.d/log-config.yaml"
    sp.getoutput(cmd)

    cmd = "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)

    time.sleep(30)

    cmd = "sudo go build " + workdirectory + "/loggeneratorscript.go"
    sp.getoutput(cmd)

    cmd = "sudo chmod +x " + workdirectory + "/loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "sudo " + workdirectory + "/loggeneratorscript" + ' ' + str(NumberofLogs) + ' ' + str(
        NumberofLogFiles) + ' ' + str(LogMsgLength) + ' ' + str(LogRotateSizeInMB) + ' ' + str(TimeToSleep)
    sp.getoutput(cmd)

    time.sleep(60)

    for i in filteringconfigfilelist:
        for k, j in i['inputs'].items():
            app = (k)
            filteringvalue = (j['filters'][0]['include'])
            filtervalue = filteringvalue.capitalize()

            filteringlogsurl = "https://"\
                + portal +\
                "/logsrql/api/v7/tenants/"\
                + tenantid +\
                "/logs?query={source={"\
                '"'\
                + app +\
                '"'\
                "}&limit=51&start="\
                + str(starttimenanosec) +\
                "&end="\
                + str(endtimenanosec)

            payload = {}
            headers = {
                'Authorization': AuthToken,
                'Content-Type': 'application/json'
            }

        filtering_response = requests.request(
            "GET", filteringlogsurl, headers=headers, data=payload)
        if filtering_response.status_code == 200:
            filteringresponsejson = filtering_response.json()
            data = filteringresponsejson['data']
            resultdata = data['result']
            for p in resultdata:
                val = (p['values'])
                for k in val:
                    message = json.loads(k[1])
                msglevel = message['level']

            loglevel = msglevel

            if loglevel == filtervalue:
                status = "Validation Pass - Filtering Logs Functionality is Working Properly"
                parsedreportfile['FilteringLogs_Functionality'] = status
            else:
                status = "Validation Fail - Filtering Logs Functionality is not Working Properly"
                parsedreportfile['FilteringLogs_Functionality'] = status
        
        else:
            status = filtering_response.reason
            parsedreportfile['FilteringLogs_Functionality'] = status        

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)

    ReomveLogsGenerator()


def ReomveLogsGenerator():
    cmd = "rm -rf loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "rm -rf *.log"
    sp.getoutput(cmd)
