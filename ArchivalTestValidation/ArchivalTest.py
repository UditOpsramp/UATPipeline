#!/usr/lib/python3

import yaml
import ruamel.yaml
import subprocess as sp
import datetime
import time


def ArchivalTesting(workdirectory, tenantid, currenttime, bucketname, ArchivalFileSize):

    currentdate = datetime.date.today().strftime("%Y-%-m-%d")
    currenthour = currenttime.hour
    dataonawsbucket = ""

    configfile = open(workdirectory + "/Logsvalidationconfig.yml")
    parsedconfigfile = yaml.load(configfile, Loader=yaml.FullLoader)

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    with open(workdirectory + "/TestCasesConfig/logs-archival.yaml", "r") as file:
        logconfigfile = yaml.load_all(file, Loader=yaml.FullLoader)
        logconfigfilelist = list(logconfigfile)

    for i in logconfigfilelist:
        for k, j in i['inputs'].items():
            (j['include'][0]) = workdirectory + "/*.log"

    logconfigfile = yaml.safe_dump_all(
        logconfigfilelist, sort_keys=False, explicit_start=True)

    yaml_new = ruamel.yaml.YAML(typ='safe')
    data = yaml_new.load(logconfigfile)

    with open(workdirectory + "/TestCasesConfig/logs-archival.yaml", "w") as file:
        yaml.dump(data, file, explicit_start=True, sort_keys=False)

    NumberofLogs = parsedconfigfile['NumberofLogs']
    NumberofLogFiles = parsedconfigfile['NumberofLogFiles']
    LogMsgLength = parsedconfigfile['LogMsgLength']
    LogRotateSizeInMB = parsedconfigfile['LogRotateSizeInMB']
    TimeToSleep = parsedconfigfile['TimeToSleep']

    cmd = "sudo cp " + workdirectory + \
        "/TestCasesConfig/logs-archival.yaml /opt/opsramp/agent/conf/log.d/log-config.yaml"
    sp.getoutput(cmd)

    cmd = "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)

    time.sleep(60)

    cmd = "sudo go build " + workdirectory + "/loggeneratorscript.go"
    sp.getoutput(cmd)

    cmd = "sudo chmod +x " + workdirectory + "/loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "sudo " + workdirectory + "/loggeneratorscript" + ' ' + str(NumberofLogs) + ' ' + str(
        NumberofLogFiles) + ' ' + str(LogMsgLength) + ' ' + str(LogRotateSizeInMB) + ' ' + str(TimeToSleep)
    sp.getoutput(cmd)

    time.sleep(30)

    cmd = "sudo ls -l --b=M  *.log | cut -d ' ' -f5"

    logfilesize = sp.getoutput(cmd)

    if logfilesize >= ArchivalFileSize:

        cmd = "sudo aws s3 ls s3://" + bucketname + "/archive/" + \
            str(tenantid) + "/" + str(currentdate) + "/" + str(currenthour) + "/"    
        dataonawsbucket = sp.getoutput(cmd)

        if dataonawsbucket != "":
            status = "Archival is Done Successfully"
            parsedreportfile['Archival_Status'] = status
        else:
            status = "Archival is Not Done Successfully"
            parsedreportfile['Archival_Status'] = status
    else:
        status = "File Size is not Reached to Defined Size" + ArchivalFileSize
        parsedreportfile['Archival_Status'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
 
    ReomveLogsGenerator()


def ReomveLogsGenerator():
    cmd = "rm -rf loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "rm -rf *.log"
    sp.getoutput(cmd)        