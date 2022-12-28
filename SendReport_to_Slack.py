#!/usr/lib/python3

import requests
import json


def send_slack_message(SLACK_WEBHOOK_URL, portal_name, currentdate,alllabelstatus,labelvaluesnotcoming, appslogsstaus, countlogsstaus, hostlogsstatus, queryfilterstatuslist,
                       notcontainsfunctionalitystatus, multifilterfunctionalitystatus, linefilterfunctionalitystatus, filteringlogsfunctionalitystatus, maskinglogsfunctionalitystatus, logalertcreationfunctionalitystatus, logalertgenerationfunctionalitystatus, logalertdeletionfunctionalitystatus, awslogsstatus, azurelogsstatus, gcplogsstatus, fluentdlogsstatus, fluentbitlogsstatus):

    FailTestCase_color = ""
    PassTestCase_color = ""
    FailTestCaseList = []
    PassTestCaseList = []
    failedtestcase = ""
    passtestcase = ""

    for i in [appslogsstaus, countlogsstaus, hostlogsstatus, notcontainsfunctionalitystatus, multifilterfunctionalitystatus, linefilterfunctionalitystatus, filteringlogsfunctionalitystatus, maskinglogsfunctionalitystatus, awslogsstatus, azurelogsstatus, gcplogsstatus, fluentdlogsstatus, fluentbitlogsstatus, logalertcreationfunctionalitystatus, logalertgenerationfunctionalitystatus, logalertdeletionfunctionalitystatus]:
        if "Fail" in i:
            FailTestCaseList.append(i)
            FailTestCase_color = "#D70000"
        else:
            if "Pass" in i:
                PassTestCaseList.append(i)
                PassTestCase_color = "#5AAF00"

    for j in [alllabelstatus,labelvaluesnotcoming]:
        if "Not" in j:
            FailTestCaseList.append(i)  
            FailTestCase_color = "#D70000"              
        else:
            PassTestCaseList.append(i)
            PassTestCase_color = "#5AAF00"


    for i in queryfilterstatuslist:
        if "Fail" in i:
            FailTestCaseList.append(i)
            FailTestCase_color = "#D70000"
        else:
            PassTestCaseList.append(i)
            PassTestCase_color = "#5AAF00"

    for j in FailTestCaseList:
        failedtestcase = failedtestcase + "\n" + j

    for j in PassTestCaseList:
        passtestcase = passtestcase + "\n" + j

    SLACK_PAYLOAD = {
        "attachments": [
            {
                "pretext": currentdate,
                "title": portal_name + " LOGS AND LOG ALERT DEFINITION AUTOMATION REPORT",
                "color": FailTestCase_color,
                "text": failedtestcase
            },
            {
                "color": PassTestCase_color,
                "text": passtestcase
            }
        ]
    }
    return requests.post(SLACK_WEBHOOK_URL, json.dumps(SLACK_PAYLOAD))

