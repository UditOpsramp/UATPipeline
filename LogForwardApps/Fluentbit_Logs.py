#!/usr/lib/python3

import requests
import yaml
import time
import subprocess as sp


def FluentBitLogs(workdirectory, AuthToken, portal, tenantid, starttimenanosec, endtimenanosec):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    cmd = "sudo systemctl restart fluent-bit"
    sp.getoutput(cmd)

    cmd = "sudo systemctl restart opsramp-agent"
    sp.getoutput(cmd)

    time.sleep(60)

    payload = {}

    headers = {
        'Authorization': AuthToken,
        'Content-Type': 'application/json'
    }

    logsurl = "https://"\
        + portal +\
        "/logsrql/api/v7/tenants/"\
        + tenantid +\
        '/logs?query={app="Fluentbit"}&limit=51&start='\
        + str(starttimenanosec) +\
        "&end="\
        + str(endtimenanosec)

    log_response = requests.request(
        "GET", logsurl, headers=headers, data=payload)
    if log_response.status_code == 200:
        logsresponsejson = log_response.json()
        logsdata = logsresponsejson['data']
        logsresultdata = logsdata['result']
        if not logsresultdata:
            status = "App Name : Fluent-bit : Validation Fail - Logs are not coming on portal"
            parsedreportfile['FluentBit_Logs'] = status
        else:
            status = "App Name : Fluent-bit : Validation Pass - Logs are coming on portal"
            parsedreportfile['FluentBit_Logs'] = status

    else:
        status = log_response.reason
        parsedreportfile['FluentBit_Logs'] = status

    cmd = "sudo systemctl stop fluent-bit"
    sp.getoutput(cmd)

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
