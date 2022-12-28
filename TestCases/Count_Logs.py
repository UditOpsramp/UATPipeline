#!/usr/lib/python3
import requests
import yaml
import ruamel.yaml
import time
import subprocess as sp

generatedlogscountvalue = 0
logscomingonportal = 0


def CountLogs(workdirectory, AuthToken, portal, tenantid, starttimeUNIX, endtimeUNIX, parsedconfigfile):

    global generatedlogscountvalue
    global logscomingonportal

    with open(workdirectory + "/TestCasesConfig/count-logconfig.yaml", "r") as file:
        countlogconfigfile = yaml.load_all(file, Loader=yaml.FullLoader)
        countlogconfigfilelist = list(countlogconfigfile)

    for i in countlogconfigfilelist:
        for k, j in i['inputs'].items():
            (j['include'][0]) = workdirectory + "/*.log"
    
    logconfigfile = yaml.safe_dump_all(countlogconfigfilelist,sort_keys=False, explicit_start=True)
    
    yaml_new = ruamel.yaml.YAML(typ='safe')
    data = yaml_new.load(logconfigfile)

    with open(workdirectory + "/TestCasesConfig/count-logconfig.yaml", "w") as file:
        yaml.dump(data, file,explicit_start=True,sort_keys=False)

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    NumberofLogs = parsedconfigfile['NumberofLogs']
    NumberofLogFiles = parsedconfigfile['NumberofLogFiles']
    LogMsgLength = parsedconfigfile['LogMsgLength']
    LogRotateSizeInMB = parsedconfigfile['LogRotateSizeInMB']
    TimeToSleep = parsedconfigfile['TimeToSleep']

    cmd = "sudo cp " + workdirectory + \
        "/TestCasesConfig/count-logconfig.yaml /opt/opsramp/agent/conf/log.d/log-config.yaml"
    sp.getoutput(cmd)

    cmd = "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)

    time.sleep(30)

    cmd = "sudo go build " + workdirectory + "/loggeneratorscript.go"
    sp.getoutput(cmd)

    cmd = "sudo chmod +x " + workdirectory + "/loggeneratorscript"
    sp.getoutput(cmd)

    # currenttime = datetime.datetime.utcnow()

    # print(currenttime)

    cmd = "sudo " + workdirectory + "/loggeneratorscript" + ' ' + str(NumberofLogs) + ' ' + str(
        NumberofLogFiles) + ' ' + str(LogMsgLength) + ' ' + str(LogRotateSizeInMB) + ' ' + str(TimeToSleep)
    sp.getoutput(cmd)

    # currenttime = datetime.datetime.utcnow()

    # print(currenttime)

    time.sleep(180)

    for i in countlogconfigfilelist:
        for k, j in i['inputs'].items():
            path = (j['include'][0])
            if not (j['app']):
                app = (k)
            else:
                app = (j['app'])

            cmd = "cat " + path + "| wc -l"
            logscountvalue = sp.getoutput(cmd)
            generatedlogscountvalue = int(logscountvalue)

            counturl = "https://"\
                + portal +\
                "/logsrql/api/v7/tenants/"\
                + tenantid +\
                "/logs/count?query={app="\
                '"'\
                + app +\
                '"'\
                "}&step=30&start="\
                + str(starttimeUNIX) +\
                "&end="\
                + str(endtimeUNIX)

            print("\nGeneratedLogsCount:", generatedlogscountvalue)

            payload = {}
            headers = {
                'Authorization': AuthToken,
                'Content-Type': 'application/json'
            }
            count_response = requests.request(
                "GET", counturl, headers=headers, data=payload)
            if count_response.status_code == 200:
                countresponsejson = count_response.json()
                countdata = countresponsejson['data']
                countresultdata = countdata['result']
                for p in countresultdata:
                    val = (p['values'])
                    for k in val:
                        logscomingonportal += (k[1])

                print("\nLogs Coming on Portal:", logscomingonportal)

                if logscomingonportal == generatedlogscountvalue:
                    status = "Validation Pass - All Logs are coming on portal"
                    parsedreportfile['Count_Logs'] = status
                else:
                    status = "Validation Fail - All Logs are not coming on portal"
                    parsedreportfile['Count_Logs'] = status

            else:
                status = count_response.reason
                parsedreportfile['Count_Logs'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)

    ReomveLogsGenerator()


def ReomveLogsGenerator():
    cmd = "rm -rf loggeneratorscript"
    sp.getoutput(cmd)

    cmd = "rm -rf *.log"
    sp.getoutput(cmd)
