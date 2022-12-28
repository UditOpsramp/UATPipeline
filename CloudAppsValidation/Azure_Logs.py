#!/usr/lib/python3
import requests
import yaml
import json
import datetime
import time


def AZURELogs(workdirectory, AuthToken, azuretoken, portal, tenantid, starttimenanosec, endtimenanosec):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    currenttime = datetime.datetime.utcnow().isoformat()

    azurepayload_json = [
        {
            "records": [
                {
                    "RoleLocation": "West Central US",
                    "resultType": "Start",
                    "callerIpAddress": "52.159.53.115",
                    "tenantId": "7d9844a2-6d02-44e2-9a00-325a7debc050",
                    "correlationId": "92784abb-0a64-4983-ae43-2e7e7bcb4f2d",
                    "category": "Administrative",
                    "level": "TRACE",
                    "identity": {
                        "claims": {
                            "appidacr": "2",
                            "http://schemas.microsoft.com/identity/claims/objectidentifier": "1eef38f1-aa56-4cc2-a4bb-93f7f9bbc70a",
                            "aud": "https://management.core.windows.net",
                            "exp": "1647337419",
                            "http://schemas.microsoft.com/identity/claims/tenantid": "7d9844a2-6d02-44e2-9a00-325a7debc050",
                            "idtyp": "app",
                            "nbf": "1647250719",
                            "aio": "E2ZgYHCc51rxnrvfiLs6gaPrXkAPAA==",
                            "http://schemas.microsoft.com/identity/claims/identityprovider": "https://sts.windows.net/7d9844a2-6d02-44e2-9a00-325a7debc050/",
                            "appid": "4962773b-9cdb-44cf-a8bf-237846a00ab7",
                            "iss": "https://sts.windows.net/7d9844a2-6d02-44e2-9a00-325a7debc050/",
                            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": "1eef38f1-aa56-4cc2-a4bb-93f7f9bbc70a",
                            "iat": "1647250719",
                            "rh": "0.AVYAokSYfQJt4kSaADJafevAUEZIf3kAutdPukPawfj2MBNWAAA.",
                            "xms_tcdt": "1483074389",
                            "ver": "1.0",
                            "uti": "cqugnLPLHkWorJon6owkAA"
                        },
                        "authorization": {
                            "action": "Microsoft.EventHub/namespaces/authorizationRules/listKeys/action",
                            "scope": "/subscriptions/c85bc23f-6112-4343-ab26-c214261a880f/resourceGroups/TestEventGroup/providers/Microsoft.EventHub/namespaces/streamEventTest/authorizationRules/RootManageSharedAccessKey",
                            "evidence": {
                                "roleAssignmentId": "8ee851ab6537475d90fe7b63b88cd663",
                                "roleDefinitionId": "7fe036d8246f48bfa78fab3ee699c8f3",
                                "principalId": "1eef38f1aa564cc2a4bb93f7f9bbc70a",
                                "role": "Azure EventGrid Service BuiltIn Role",
                                "roleAssignmentScope": "/subscriptions/c85bc23f-6112-4343-ab26-c214261a880f",
                                "principalType": "ServicePrincipal"
                            }
                        }
                    },
                    "resultSignature": "Started.",
                    "durationMs": "0",
                    "resourceId": "/SUBSCRIPTIONS/C85BC23F-6112-4343-AB26-C214261A880F/RESOURCEGROUPS/TESTEVENTGROUP/PROVIDERS/MICROSOFT.EVENTHUB/NAMESPACES/STREAMEVENTTEST/AUTHORIZATIONRULES/ROOTMANAGESHAREDACCESSKEY",
                    "properties": {
                        "entity": "/subscriptions/c85bc23f-6112-4343-ab26-c214261a880f/resourceGroups/TestEventGroup/providers/Microsoft.EventHub/namespaces/streamEventTest/authorizationRules/RootManageSharedAccessKey",
                        "hierarchy": "7d9844a2-6d02-44e2-9a00-325a7debc050/c85bc23f-6112-4343-ab26-c214261a880f",
                        "message": "Microsoft.EventHub/namespaces/authorizationRules/listKeys/action",
                        "eventCategory": "Administrative"
                    },
                    "operationName": "MICROSOFT.EVENTHUB/NAMESPACES/AUTHORIZATIONRULES/LISTKEYS/ACTION",
                    "time": currenttime + 'Z',
                    "ReleaseVersion": "6.2022.10.2+421507d1efb41ada88441f9af51c650598e3572f.release_2022w10"
                }
            ]
        }
    ]

    for i in azurepayload_json:
        for j in i['records']:
            operationName = j['operationName']

    azurelogsgenerating_url = "https://"\
        + portal +\
        "/logs/api/v1/tenants/"\
        + tenantid +\
        "/logs?source=azure&token="\
        + azuretoken

    payload = json.dumps(azurepayload_json)

    headers = {
        'Authorization': AuthToken,
        'Content-Type': 'application/json'
    }

    azurelogsgenerating_response = requests.request(
        "POST", azurelogsgenerating_url, headers=headers, data=payload)

    print(azurelogsgenerating_response.text)

    time.sleep(60)

    logsurl = "https://"\
        + portal +\
        "/logsrql/api/v7/tenants/"\
        + tenantid +\
        "/logs?query={operationName="\
        '"'\
        + operationName +\
        '"'\
        "}&limit=51&start="\
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
            status = "App Name : " + 'AZURE' + \
                " : Validation Fail - Logs are not coming on portal"
            parsedreportfile['AZURE_Logs'] = status
        else:
            status = "App Name : " + "AZURE" + " : Validation Pass - Logs are coming on portal"
            parsedreportfile['AZURE_Logs'] = status

    else:
        status = log_response.reason
        parsedreportfile['AZURE_Logs'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
