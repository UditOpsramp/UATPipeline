#!/usr/lib/python3
import requests
import yaml
import json
import gzip
import base64
import datetime
import calendar
import time

def AWSLogs(workdirectory, AuthToken, awstoken, portal, tenantid, starttimenanosec, endtimenanosec):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    currenttime = datetime.datetime.utcnow()
    starttimeUNIX = calendar.timegm(currenttime.timetuple())
    starttime = starttimeUNIX * 1000

    awspayload_json = {"messageType": "DATA_MESSAGE", "owner": "320444959714", "host": "host", "logGroup": "opsramplog2", "logStream": "i-03114b2eeeecqiboio", "subscriptionFilters": ["otherlogmanagement"], "logEvents": [
        {"id": "36711867709451338316221380620199828540099109097369894912", "timestamp": starttime, "message": "Apr  12 10:31:23 ip-172-31-92-154 dhclient[2752]: XMT: Solicit on eth0, interval 126290ms."}]}
    json_str = json.dumps(awspayload_json).encode()
    gzipcompress = gzip.compress(json_str)
    convertobase64 = base64.encodebytes(gzipcompress)
    decode_awspayload = convertobase64.decode()

    awslogsgenerating_url = "https://"\
        + portal +\
        "/logs/api/v1/tenants/"\
        + tenantid +\
        "/logs?source=aws&token="\
        + awstoken

    payload = json.dumps({
        "requestId": "0d546767-1b9d-46e6-a474-878d3ed7d25a",
        "timestamp": starttime,
        "records": [
            {
                "data": decode_awspayload
            }
        ]
    })

    headers = {
        'Authorization': AuthToken,
        'Content-Type': 'application/json'
    }

    awslogsgenerating_response = requests.request(
        "POST", awslogsgenerating_url, headers=headers, data=payload)
    print(awslogsgenerating_response.text)

    logGroup = awspayload_json['logGroup']

    time.sleep(60)

    logsurl = "https://"\
        + portal +\
        "/logsrql/api/v7/tenants/"\
        + tenantid +\
        "/logs?query={logGroup="\
        '"'\
        + logGroup +\
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
            status = "App Name : " + 'AWS' + " : Validation Fail - Logs are not coming on portal"
            parsedreportfile['AWS_Logs'] = status
        else:
            status = "App Name : " + "AWS" + " : Validation Pass - Logs are coming on portal"
            parsedreportfile['AWS_Logs'] = status

    else:
        status = log_response.reason
        parsedreportfile['AWS_Logs'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
