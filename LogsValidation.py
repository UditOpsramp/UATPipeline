#!/usr/lib/python3
import yaml
import datetime
import calendar
import os
import GetAuthToken
import TestCases.Apps_Logs
import TestCases.Count_Logs
import TestCases.Hosts_Logs
import TestCases.QueryFilters
import TestCases.Labels
import TestCases.Label_Values
import TestCases.FilteringLogs
import TestCases.MultiFilters
import TestCases.NotContainsFilter
import TestCases.LineFilter
import TestCases.MaskingLogs
import AlertDefintionValidation.Createalertdef
import AlertDefintionValidation.GetAlertDetails
import AlertDefintionValidation.DeleteAlertDefinition
import CloudAppsValidation.AWS_Logs
import CloudAppsValidation.Azure_Logs
import CloudAppsValidation.GCP_Logs
import LogForwardApps.Fluentd_Logs
import LogForwardApps.Fluentbit_Logs
import SendReport_to_GooleChat
import SendReport_to_Slack

workdirectory = os.getcwd()

configfile = open(workdirectory + "/Logsvalidationconfig.yml")
parsedconfigfile = yaml.load(configfile, Loader=yaml.FullLoader)
portal = parsedconfigfile["portal_url"]
tenantid = parsedconfigfile["client_id"]
clientkey = parsedconfigfile["client_key"]
clientsecret = parsedconfigfile["client_secret"]
awstoken = parsedconfigfile["AWS_TOKEN"]
azuretoken = parsedconfigfile["AZURE_TOKEN"]
gcptoken = parsedconfigfile["GCP_TOKEN"]
googlechat_webhook_url = parsedconfigfile["GOOGLECHAT_WEBHOOK_URL"]
slack_webhook_url = parsedconfigfile["SLACK_WEBHOOK_URL"]
portal_name = parsedconfigfile['Portal_Name']

currentdate = datetime.date.today().strftime("%d %b %Y")
currenttime = datetime.datetime.utcnow()
starttimeUNIX = calendar.timegm(currenttime.timetuple())
starttimenanosec = starttimeUNIX * 1000000000
endtime = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
endtimeUNIX = calendar.timegm(endtime.timetuple())
endtimenanosec = endtimeUNIX * 1000000000

# Put Hash before the Test Case to Skip (Example #TestCases.Apps_Logs.AppLogs)

GetAuthToken.GetAuthToken(clientkey, clientsecret, portal)
AuthToken = GetAuthToken.token

TESTCASE1 = "\nTEST CASE-1 : VALIDATION OF AWS LOGS\n\n"
CloudAppsValidation.AWS_Logs.AWSLogs(
    workdirectory, AuthToken, awstoken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE2 = "\n\nTEST CASE-2 : VALIDATION OF AZURE LOGS\n\n"
CloudAppsValidation.Azure_Logs.AZURELogs(
    workdirectory, AuthToken, azuretoken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE3 = "\n\nTEST CASE-3 : VALIDATION OF GCP LOGS\n\n"
CloudAppsValidation.GCP_Logs.GCPLogs(
    workdirectory, AuthToken, gcptoken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE4 = "\n\nTESTCASE-4 : CHECK ALL LABELS COMING OR NOT\n"   
TestCases.Labels.LabelsTest(workdirectory,AuthToken,tenantid,portal,starttimeUNIX,endtimeUNIX)

TESTCASE5 = "\n\nTESTCASE-5 : CHECK ALL LABELS-VALUES COMING OR NOT\n"   
TestCases.Label_Values.LabelValues(workdirectory, AuthToken, tenantid, portal, starttimeUNIX, endtimeUNIX)

TESTCASE6 = "\n\nTEST CASE-6 : VALIDATION OF APP'S LOGS\n\n"
TestCases.Apps_Logs.AppLogs(
    workdirectory, AuthToken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE7 = "\n\nTEST CASE-7 : VALIDATION OF COUNT OF LOGS\n\n"
TestCases.Count_Logs.CountLogs(
    workdirectory, AuthToken, portal, tenantid, starttimeUNIX, endtimeUNIX, parsedconfigfile)

TESTCASE8 = "\n\nTEST CASE-8 : VALIDATION OF LOGS FOR EACH HOST\n\n"
TestCases.Hosts_Logs.HostLogs(workdirectory, AuthToken, tenantid, portal,
                              starttimeUNIX, endtimeUNIX, starttimenanosec, endtimenanosec)

TESTCASE9 = "\n\nTEST CASE-9 : VALIDATION OF NOT CONTAINS FILTER FUNCTIONALITY\n\n"
TestCases.NotContainsFilter.QueryNotContainsLogs(
    workdirectory, AuthToken, portal, tenantid, starttimenanosec, endtimenanosec, parsedconfigfile)

TESTCASE10 = "\n\nTEST CASE-10 : VALIDATION OF MULTI-FILTERING FUNCTIONALITY\n\n"
TestCases.MultiFilters.MultiFilter(
    workdirectory, AuthToken, tenantid, portal, starttimenanosec, endtimenanosec)

TESTCASE11 = "\n\nTEST CASE-11 : VALIDATION OF LINE-FILTERING FUNCTIONALITY\n\n"
TestCases.LineFilter.LineFilter(
    workdirectory, AuthToken, tenantid, portal, starttimenanosec, endtimenanosec)

TESTCASE12 = "\n\nTEST CASE-12 : VALIDATION OF FILTERING LOGS FUNCTIONALITY\n\n"
TestCases.FilteringLogs.FilteringLogs(
    workdirectory, AuthToken, tenantid, portal, starttimenanosec, endtimenanosec, parsedconfigfile)

TESTCASE13 = "\n\nTEST CASE-13 : VALIDATION OF MASKING LOGS FUNCTIONALITY\n\n"
TestCases.MaskingLogs.MaskingLogs(
    workdirectory, AuthToken, tenantid, portal, parsedconfigfile, starttimenanosec, endtimenanosec)

TESTCASE14 = "\n\nTEST CASE-14 : VALIDATION OF FLUENTD LOGS\n\n"
LogForwardApps.Fluentd_Logs.FluentDLogs(
    workdirectory, AuthToken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE15 = "\n\nTEST CASE-15 : VALIDATION OF FLUENT-BIT LOGS\n\n"
LogForwardApps.Fluentbit_Logs.FluentBitLogs(
    workdirectory, AuthToken, portal, tenantid, starttimenanosec, endtimenanosec)

TESTCASE16 = "\n\nTEST CASE-16 : VALIDATION OF QUERY FILTERS FUNCTIONALITY FOR EACH ATTRIBUTE"
TestCases.QueryFilters.QueryFilter(
    workdirectory, AuthToken, tenantid, portal, starttimeUNIX, endtimeUNIX, starttimenanosec, endtimenanosec)

TESTCASE17 = "\n\nTEST CASE-17 : VALIDATION OF CREATION OF LOG-ALERT DEFINITION\n\n"
AlertDefintionValidation.Createalertdef.CreateLogAlertDefinition(
    workdirectory, AuthToken, portal, tenantid)

TESTCASE18 = "\n\nTEST CASE-18 : VALIDATION OF ALERT GENERATION\n\n"
AlertDefintionValidation.GetAlertDetails.GetAlertDetails(
    workdirectory, AuthToken, portal, tenantid)

TESTCASE19 = "\n\nTEST CASE-19 : VALIDATION OF DELETION OF LOG-ALERT DEFINITION\n\n"
AlertDefintionValidation.DeleteAlertDefinition.DeleteLogAlertDefinition(
    workdirectory, AuthToken, portal, tenantid)

reportfile = open(workdirectory + "/Report.yml")
parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

GeneratedLogsCount = TestCases.Count_Logs.generatedlogscountvalue
Logscomingonportal = TestCases.Count_Logs.logscomingonportal

alllabelstatus = parsedreportfile['AllLabelStatus']
labelvaluesnotcoming = parsedreportfile['LabelValuesNotComing']
appslogsstaus = parsedreportfile['Source_Logs']
countlogsstaus = parsedreportfile['Count_Logs']
hostlogsstatus = parsedreportfile['Host_Logs']
queryfilterstatuslist = parsedreportfile['QueryFilter_Functionality']
notcontainsfunctionalitystatus = parsedreportfile['NotContains_Functionality']
multifilterfunctionalitystatus = parsedreportfile['MultiFilter_Functionalty']
linefilterfunctionalitystatus = parsedreportfile['LineFilter_Functionality']
filteringlogsfunctionalitystatus = parsedreportfile['FilteringLogs_Functionality']
maskinglogsfunctionalitystatus = parsedreportfile['MaskingLogs_Functionality']
logalertcreationfunctionalitystatus = parsedreportfile['LogAlertCreation']
logalertgenerationfunctionalitystatus = parsedreportfile['LogAlertGeneration']
logalertdeletionfunctionalitystatus = parsedreportfile['LogAlertDeletion']
awslogsstatus = parsedreportfile['AWS_Logs']
azurelogsstatus = parsedreportfile['AZURE_Logs']
gcplogsstatus = parsedreportfile['GCP_Logs']
fluentdlogsstatus = parsedreportfile['FluentD_Logs']
fluentbitlogsstatus = parsedreportfile['FluentBit_Logs']

GOOGLECHAT_WEBHOOK_URL = googlechat_webhook_url

SLACK_WEBHOOK_URL = slack_webhook_url

SendReport_to_GooleChat.send_googlechat_message(GOOGLECHAT_WEBHOOK_URL, portal_name, currentdate, TESTCASE1, TESTCASE2, TESTCASE3, TESTCASE4, TESTCASE5, TESTCASE6, TESTCASE7, TESTCASE8, TESTCASE9, TESTCASE10, TESTCASE11, TESTCASE12, TESTCASE13, TESTCASE14, TESTCASE15, TESTCASE16, TESTCASE17,TESTCASE18,TESTCASE19, alllabelstatus, labelvaluesnotcoming, appslogsstaus, countlogsstaus, GeneratedLogsCount, Logscomingonportal, hostlogsstatus, queryfilterstatuslist,
                                                notcontainsfunctionalitystatus, multifilterfunctionalitystatus, linefilterfunctionalitystatus, filteringlogsfunctionalitystatus, maskinglogsfunctionalitystatus, logalertcreationfunctionalitystatus, logalertgenerationfunctionalitystatus, logalertdeletionfunctionalitystatus, awslogsstatus, azurelogsstatus, gcplogsstatus, fluentdlogsstatus, fluentbitlogsstatus)

SendReport_to_Slack.send_slack_message(SLACK_WEBHOOK_URL, portal_name, currentdate,alllabelstatus,labelvaluesnotcoming, appslogsstaus, countlogsstaus, hostlogsstatus, queryfilterstatuslist,
                                       notcontainsfunctionalitystatus, multifilterfunctionalitystatus, linefilterfunctionalitystatus, filteringlogsfunctionalitystatus, maskinglogsfunctionalitystatus, logalertcreationfunctionalitystatus, logalertgenerationfunctionalitystatus, logalertdeletionfunctionalitystatus, awslogsstatus, azurelogsstatus, gcplogsstatus, fluentdlogsstatus, fluentbitlogsstatus)

parsedreportfile['QueryFilter_Functionality'] = []
parsedreportfile['AllLabelStatus'] = []
parsedreportfile['LabelValuesNotComing'] = []
with open(workdirectory + "/Report.yml", "w") as file:
    yaml.dump(parsedreportfile, file)
