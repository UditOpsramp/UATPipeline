#!/usr/lib/python3
import requests
import json
import yaml


def CreateLogAlertDefinition(workdirectory, AuthToken, portal, tenantid):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    createurl = "https://"\
        + portal +\
        "/log-alert/api/v1/alerts/tenants/"\
        + tenantid +\
        "/add"

    payload = json.dumps({
        "alert": {
            "name": "LogAlertTest",
            "type": "log",
            "tenantId": tenantid,
            "conditions": [
                {
                    "severity": "critical",
                    "operator": ">",
                    "value": 1,
                    "duration": {
                        "value": 30,
                        "unit": "minute"
                    }
                }
            ],
            "notification": {
                "subject": "LogAlertTest",
                "description": "LogAlertTest"
            },
            "query": "{level=\"Debug\"}"
        },
        "tenantId": tenantid
    })

    headers = {
        'Authorization': AuthToken,
        'Content-Type': 'text/plain'
    }

    response = requests.request(
        "POST", createurl, headers=headers, data=payload)
    if response.status_code == 200:
        status = "Validation Pass - Log Alert Definiton Created Successfully"
        parsedreportfile['LogAlertCreation'] = status
    else:
        status = "Validation Fail - Log Alert Defintion Not Created Successfully"
        parsedreportfile['LogAlertCreation'] = status
    jsonreponse = response.json()

    alertid = jsonreponse['alert']['alertId']

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)

    with open(workdirectory + "/AlertDefintionValidation/alertinfo.yml", "w") as file:
        file.write("AlertComponent" + ': ' + alertid + "\n")
