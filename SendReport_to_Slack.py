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
                
    for j in [alllabelstatus]:
        for m in j :
            if "Not" in m:
                FailTestCaseList.append(m)  
                FailTestCase_color = "#D70000"              
            else:
                PassTestCaseList.append(m)
                PassTestCase_color = "#5AAF00"
    
    for k in [labelvaluesnotcoming]:
        for n in k :
            if "Not" in n:
                FailTestCaseList.append(n)  
                FailTestCase_color = "#D70000"              
            else:
                PassTestCaseList.append(n)
                PassTestCase_color = "#5AAF00"   
        
    for i in queryfilterstatuslist:
        if "Fail" in i:
            FailTestCaseList.append(i)
            FailTestCase_color = "#D70000"
        else:
            PassTestCaseList.append(i)
            PassTestCase_color = "#5AAF00"

    for l in FailTestCaseList:
        failedtestcase = failedtestcase + "\n" + l

    for l in PassTestCaseList:
        passtestcase = passtestcase + "\n" + l

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

