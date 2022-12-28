#!/usr/lib/python3
import requests
import yaml
import time
import subprocess as sp

def AppLogs(workdirectory,AuthToken,portal,tenantid,starttimenanosec,endtimenanosec):
    
    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile,Loader=yaml.FullLoader)

    time.sleep(60)

    cmd= "sudo cp " + workdirectory + "/TestCasesConfig/app-logconfig.yaml /opt/opsramp/agent/conf/log.d/log-config.yaml"
    sp.getoutput(cmd)
   
    cmd= "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)
    
    time.sleep(30)

    with open(workdirectory + "/TestCasesConfig/app-logconfig.yaml","r") as file :
        logconfigfile = yaml.load_all(file,Loader=yaml.FullLoader)
        logconfigfilelist= list(logconfigfile)
     
    for i in logconfigfilelist:
        for k,j in i['inputs'].items():
            if not (j['app']):
                app = (k)
            else:    
                app = (j['app']) 
        
            payload={}
            headers = {
                'Authorization': AuthToken,
                'Content-Type': 'application/json'
            } 
        
            logsurl = "https://"\
            +portal+\
            "/logsrql/api/v7/tenants/"\
            +tenantid+\
            "/logs?query={app="\
            '"'\
            +app+\
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
                    status = "App Name : " + app + " : Validation Fail - Logs are not coming on portal"
                    parsedreportfile['Apps_Logs'] = status
                else:
                    status = "App Name : " + app + " : Validation Pass - Logs are coming on portal"
                    parsedreportfile['Apps_Logs'] = status

            else:
                status = log_response.text
                parsedreportfile['Apps_Logs'] = status

    with open(workdirectory + "/Report.yml","w") as file :
        yaml.dump(parsedreportfile,file)
