#!/usr/lib/python3
import requests
import json
import yaml
import ruamel.yaml
import time
import subprocess as sp

def MaskingLogs(workdirectory,AuthToken,tenantid,portal,parsedconfigfile,starttimenanosec,endtimenanosec) :

    with open(workdirectory + "/TestCasesConfig/log-masking.yaml","r") as file :
        maskingconfigfile = yaml.load_all(file,Loader=yaml.FullLoader)
        maskingconfigfilelist= list(maskingconfigfile)
    
    for i in maskingconfigfilelist:
        for k,j in i['inputs'].items():
            (j['include'][0]) = workdirectory + "/*.log"  
    
    logconfigfile = yaml.safe_dump_all(maskingconfigfilelist,sort_keys=False, explicit_start=True)
    
    yaml_new = ruamel.yaml.YAML(typ='safe')
    data = yaml_new.load(logconfigfile)
    
    with open(workdirectory + "/TestCasesConfig/log-masking.yaml","w") as file :
        yaml.dump(data, file,explicit_start=True,sort_keys=False)

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile,Loader=yaml.FullLoader)  

    NumberofLogs = parsedconfigfile['NumberofLogs']
    NumberofLogFiles = parsedconfigfile['NumberofLogFiles']
    LogMsgLength = parsedconfigfile['LogMsgLength']
    LogRotateSizeInMB = parsedconfigfile['LogRotateSizeInMB']
    TimeToSleep = parsedconfigfile['TimeToSleep']

    cmd= "sudo cp " + workdirectory + "/TestCasesConfig/log-masking.yaml /opt/opsramp/agent/conf/log.d/log-config.yaml"
    sp.getoutput(cmd)
    
    cmd= "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)
    
    time.sleep(30)
    
    cmd = "sudo go build " + workdirectory + "/loggeneratorscript.go"
    sp.getoutput(cmd)

    cmd = "sudo chmod +x " + workdirectory + "/loggeneratorscript"
    sp.getoutput(cmd)
    
    cmd = "sudo " + workdirectory + "/loggeneratorscript"+ ' ' + str(NumberofLogs) + ' ' + str(NumberofLogFiles) + ' ' + str(LogMsgLength) +  ' '     + str(LogRotateSizeInMB) + ' ' + str(TimeToSleep)
    sp.getoutput(cmd)
    
    time.sleep(60)
   
    global logmessage
    for i in maskingconfigfilelist:

        for k,j in i['inputs'].items():
            app = (j['app'])
            maskingmessage = (j['masking'][0]['placeholder']) 

            maskinglogsurl = "https://"\
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
            
            payload={}
            headers = {
                'Authorization': AuthToken,
                'Content-Type': 'application/json'
            }       
            
        masking_response = requests.request("GET", maskinglogsurl, headers=headers, data=payload)
        if masking_response.status_code == 200:
            maskingresponsejson = masking_response.json()
            maskingdata = maskingresponsejson['data']
            maskingresultdata = maskingdata['result'] 
            for p in maskingresultdata:
                val = (p['values'])
                for k in val:
                    message = json.loads(k[1])  
                logmessage = message['message'] 
              
            if logmessage == maskingmessage:    
                status = "Validation Pass - Masking Logs Functionality is Working Properly"
                parsedreportfile['MaskingLogs_Functionality'] = status                    
            else:
                status = "Validation Fail - Masking Logs Functionality is not Working Properly"
                parsedreportfile['MaskingLogs_Functionality'] = status  
        
        else:
            status = masking_response.reason
            parsedreportfile['MaskingLogs_Functionality'] = status
                        
    with open(workdirectory + "/Report.yml","w") as file :
        yaml.dump(parsedreportfile,file)

    ReomveLogsGenerator()

def ReomveLogsGenerator() :
    cmd = "rm -rf loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "rm -rf *.log"
    sp.getoutput(cmd)

