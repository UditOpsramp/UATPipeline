#!/usr/lib/python3

import requests


def send_googlechat_message(GOOGLECHAT_WEBHOOK_URL, portal_name, currentdate, TESTCASE1, TESTCASE2, TESTCASE3, TESTCASE4, TESTCASE5, TESTCASE6, TESTCASE7, TESTCASE8, TESTCASE9, TESTCASE10, TESTCASE11, TESTCASE12, TESTCASE13, TESTCASE14, TESTCASE15, TESTCASE16, TESTCASE17, TESTCASE18, TESTCASE19, alllabelstatus,labelvaluesnotcoming, appslogsstaus, countlogsstaus, GeneratedLogsCount, Logscomingonportal, hostlogsstatus, queryfilterstatuslist,
                                              notcontainsfunctionalitystatus, multifilterfunctionalitystatus, linefilterfunctionalitystatus, filteringlogsfunctionalitystatus, maskinglogsfunctionalitystatus, logalertcreationfunctionalitystatus, logalertgenerationfunctionalitystatus, logalertdeletionfunctionalitystatus, awslogsstatus, azurelogsstatus, gcplogsstatus, fluentdlogsstatus, fluentbitlogsstatus):
    
    if "Pass" in awslogsstatus:
        test1status = '<b><font color=\"#5AAF00\">' + awslogsstatus + '</font></b>'
    else:
        test1status = '<b><font color=\"#D70000\">' + awslogsstatus + '</font></b>'

    if "Pass" in azurelogsstatus:
        test2status = '<b><font color=\"#5AAF00\">' + azurelogsstatus + '</font></b>'
    else:
        test2status = '<b><font color=\"#D70000\">' + azurelogsstatus + '</font></b>'

    if "Pass" in gcplogsstatus:
        test3status = '<b><font color=\"#5AAF00\">' + gcplogsstatus + '</font></b>'
    else:
        test3status = '<b><font color=\"#D70000\">' + gcplogsstatus + '</font></b>'
        
    test4status = ''
    for i in alllabelstatus : 
        if "Not" in i:
            labelstatus = '<b><font color=\"#D70000\">' + \
            i + '</font></b>'
            test4status = test4status + "\n" + labelstatus
        else:
            labelstatus = '<b><font color=\"#5AAF00\">' + \
            i + '</font></b>'
            test4status = test4status + "\n" + labelstatus
            
    test5status = ''
    for i in labelvaluesnotcoming : 
        if "Not" in i:
            labelvaluestatus = '<b><font color=\"#D70000\">' + \
            i + '</font></b>'
            test5status = test5status + "\n" + labelvaluestatus
        else:
            labelvaluestatus = '<b><font color=\"#5AAF00\">' + \
            i + '</font></b>'
            test5status = test5status + "\n" + labelvaluestatus         
                
    if "Pass" in appslogsstaus:
        test6status = '<b><font color=\"#5AAF00\">' + appslogsstaus + '</font></b>'
    else:
        test6status = '<b><font color=\"#D70000\">' + appslogsstaus + '</font></b>'

    if "Pass" in countlogsstaus:
        test7status = '<b><font color=\"#5AAF00\">' + countlogsstaus + '</font></b>'
    else:
        test7status = '<b><font color=\"#D70000\">' + countlogsstaus + '</font></b>'

    if "Pass" in hostlogsstatus:
        test8status = '<b><font color=\"#5AAF00\">' + hostlogsstatus + '</font></b>'
    else:
        test8status = '<b><font color=\"#D70000\">' + hostlogsstatus + '</font></b>'

    if "Pass" in notcontainsfunctionalitystatus:
        test9status = '<b><font color=\"#5AAF00\">' + \
            notcontainsfunctionalitystatus + '</font></b>'
    else:
        test9status = '<b><font color=\"#D70000\">' + \
            notcontainsfunctionalitystatus + '</font></b>'

    if "Pass" in multifilterfunctionalitystatus:
        test10status = '<b><font color=\"#5AAF00\">' + \
            multifilterfunctionalitystatus + '</font></b>'
    else:
        test10status = '<b><font color=\"#D70000\">' + \
            multifilterfunctionalitystatus + '</font></b>'

    if "Pass" in linefilterfunctionalitystatus:
        test11status = '<b><font color=\"#5AAF00\">' + \
            linefilterfunctionalitystatus + '</font></b>'
    else:
        test11status = '<b><font color=\"#D70000\">' + \
            linefilterfunctionalitystatus + '</font></b>'

    if "Pass" in filteringlogsfunctionalitystatus:
        test12status = '<b><font color=\"#5AAF00\">' + \
            filteringlogsfunctionalitystatus + '</font></b>'
    else:
        test12status = '<b><font color=\"#D70000\">' + \
            filteringlogsfunctionalitystatus + '</font></b>'

    if "Pass" in maskinglogsfunctionalitystatus:
        test13status = '<b><font color=\"#5AAF00\">' + \
            maskinglogsfunctionalitystatus + '</font></b>'
    else:
        test13status = '<b><font color=\"#D70000\">' + \
            maskinglogsfunctionalitystatus + '</font></b>'

    if "Pass" in fluentdlogsstatus:
        test14status = '<b><font color=\"#5AAF00\">' + fluentdlogsstatus + '</font></b>'
    else:
        test14status = '<b><font color=\"#D70000\">' + fluentdlogsstatus + '</font></b>'

    if "Pass" in fluentbitlogsstatus:
        test15status = '<b><font color=\"#5AAF00\">' + \
            fluentbitlogsstatus + '</font></b>'
    else:
        test15status = '<b><font color=\"#D70000\">' + \
            fluentbitlogsstatus + '</font></b>'
               
    test16status = ''
    for j in queryfilterstatuslist:
        if "Pass" in j:
            queryfilterstatus = '<b><font color=\"#5AAF00\">' + j + '</font></b>'
            test16status = test16status + "\n" + queryfilterstatus
        else:
            queryfilterstatus = '<b><font color=\"#D70000\">' + i + '</font></b>'
            test16status = test16status + "\n" + queryfilterstatus

    if "Pass" in logalertcreationfunctionalitystatus:
        test17status = '<b><font color=\"#5AAF00\">' + \
            logalertcreationfunctionalitystatus + '</font></b>'
    else:
        test17status = '<b><font color=\"#D70000\">' + \
            logalertcreationfunctionalitystatus + '</font></b>'

    if "Pass" in logalertgenerationfunctionalitystatus:
        test18status = '<b><font color=\"#5AAF00\">' + \
            logalertgenerationfunctionalitystatus + '</font></b>'
    else:
        test18status = '<b><font color=\"#D70000\">' + \
            logalertgenerationfunctionalitystatus + '</font></b>'

    if "Pass" in logalertdeletionfunctionalitystatus:
        test19status = '<b><font color=\"#5AAF00\">' + \
            logalertdeletionfunctionalitystatus + '</font></b>'
    else:
        test19status = '<b><font color=\"#D70000\">' + \
            logalertdeletionfunctionalitystatus + '</font></b>'
            
    WEBHOOK_URL = GOOGLECHAT_WEBHOOK_URL
    title = portal_name + " LOGS AND LOG ALERT DEFINITION AUTOMATION REPORT"
    subtitle = currentdate
    
    paragraph =  '<b>' + TESTCASE1 + '</b>' + test1status + '<b>' + TESTCASE2 + test2status + '<b>' + TESTCASE3 + test3status + '<b>' + TESTCASE4 + test4status + '<b>' + TESTCASE5 + test5status + '<b>' + TESTCASE6 + test6status +  '<b>' + TESTCASE7 + "INGESTED-LOGS-COUNT : " + str(GeneratedLogsCount) + "\n\n" + "UI-LOGS-COUNT: " + str(Logscomingonportal) + "\n\n" + test7status + '<b>' + TESTCASE8 + test8status + '<b>' + TESTCASE9 + test9status + '<b>' + TESTCASE10 + \
        test10status + '<b>' + TESTCASE11 + test11status + '<b>' + TESTCASE12 + test12status + '<b>' + TESTCASE13 + test13status + '<b>' + TESTCASE14 + test14status + \
       '<b>' + TESTCASE15 + test15status + '<b>' + TESTCASE16 + \
        test16status + '<b>' + TESTCASE17 + \
        test17status + '<b>' + TESTCASE18 + test18status + '<b>' + TESTCASE19 + test19status
    widget = {'textParagraph': {'text': paragraph}}
    res = requests.post(
        WEBHOOK_URL,
        json={
            'cards': [
                {
                    'header': {
                        'title': title,
                        'subtitle': subtitle,
                    },
                    'sections': [{'widgets': [widget]}],
                }
            ]
        },
    )
