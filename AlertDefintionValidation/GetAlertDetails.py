#!/usr/lib/python3
import requests
import yaml
import time


def GetAlertDetails(workdirectory, AuthToken, portal, tenantid):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    alertinfofile = open(
        workdirectory + "/AlertDefintionValidation/alertinfo.yml")
    parsedalertinfofile = yaml.load(alertinfofile, Loader=yaml.FullLoader)
    AlertComponent = parsedalertinfofile['AlertComponent']

    time.sleep(420)

    url = "https://"\
        + portal + \
        "/api/v2/tenants/"\
        + tenantid + \
        "/alerts/search"\

    payload = {'queryString': 'metrics:'+"LogAlertTest"}

    headers = {
        'Authorization': 'Bearer' + AuthToken,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, params=payload)
    if response.status_code == 200:
        json = response.json()
        results = json['results']
        for i in results:
            alertcomponent = i['component']
            break
        if alertcomponent == AlertComponent:
            status = "Validation Pass - Alert Generated Successfully"
            parsedreportfile['LogAlertGeneration'] = status
        else:
            status = "Validation Fail - Alert Not Generated Successfully"
            parsedreportfile['LogAlertGeneration'] = status

    else:
        status = response.reason
        parsedreportfile['LogAlertGeneration'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
