#!/usr/lib/python3
import requests
import yaml
import json
import base64
import datetime
import time


def GCPLogs(workdirectory, AuthToken, gcptoken, portal, tenantid, starttimenanosec, endtimenanosec):

    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile, Loader=yaml.FullLoader)

    currenttime = datetime.datetime.utcnow().isoformat()

    gcppayload_json = {
        "insertId": "qfbb8f0f9y1c7swc",
        "labels": {
            "compute.googleapis.com/resource_name": "gke-chaos-mesh-poc-default-pool-761fe956-plcc",
            "k8s-pod/app_kubernetes_io/component": "controller-manager",
            "k8s-pod/app_kubernetes_io/instance": "chaos-mesh",
            "k8s-pod/app_kubernetes_io/name": "chaos-mesh",
            "k8s-pod/app_kubernetes_io/part-of": "chaos-mesh",
            "k8s-pod/app_kubernetes_io/version": "2.1.3",
            "k8s-pod/pod-template-hash": "5f657fc99c"
        },
        "logName": "projects/dev-project-cloud/logs/stderr",
        "receiveTimestamp": "2022-03-22T03:04:04.70088466Z",
        "resource": {
            "labels": {
                "cluster_name": "chaos-mesh-poc",
                "container_name": "chaos-mesh",
                "location": "us-central1-c",
                "namespace_name": "chaos-testing",
                "pod_name": "chaos-controller-manager-5f657fc99c-7ghvc",
                "project_id": "dev-project-cloud"
            },
            "type": "k8s_container"
        },
        "severity": "ERROR",
        "textPayload": "2022/03/22 03:03:57 [Fx] PROVIDE\t*manager.Options <= github.com/chaos-mesh/chaos-mesh/cmd/chaos-controller-manager/provider.NewOption()",
        "timestamp": currenttime + 'Z'
    }
    json_str = json.dumps(gcppayload_json).encode()
    convertobase64 = base64.encodebytes(json_str)
    decode_gcppayload = convertobase64.decode()

    logName = gcppayload_json['logName']

    gcplogsgenerating_url = "https://"\
        + portal +\
        "/logs/api/v1/tenants/"\
        + tenantid +\
        "/logs?source=gcp&token="\
        + gcptoken

    payload = json.dumps({
        "message": {
            "attributes": {
                "logging.googleapis.com/timestamp": "2022-11-24T14:14:06.266654357Z"
            },
            "data": decode_gcppayload,
            "messageId": "6337268397087412",
            "message_id": "6337268397087412",
            "publishTime": "2022-11-24T14:14:11.551Z",
            "publish_time": "2022-11-24T14:14:11.551Z"
        },
        "subscription": "projects/dev-project-cloud/subscriptions/logStream"
    })

    headers = {
        'Authorization': AuthToken,
        'Content-Type': 'application/json'
    }

    gcplogsgenerating_response = requests.request(
        "POST", gcplogsgenerating_url, headers=headers, data=payload)
    print(gcplogsgenerating_response.text)

    time.sleep(60)

    logsurl = "https://"\
        + portal +\
        "/logsrql/api/v7/tenants/"\
        + tenantid +\
        "/logs?query={logName="\
        '"'\
        + logName +\
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
            status = "App Name : " + 'GCP' + " : Validation Fail - Logs are not coming on portal"
            parsedreportfile['GCP_Logs'] = status
        else:
            status = "App Name : " + "GCP" + " : Validation Pass - Logs are coming on portal"
            parsedreportfile['GCP_Logs'] = status

    else:
        status = log_response.reason
        parsedreportfile['GCP_Logs'] = status

    with open(workdirectory + "/Report.yml", "w") as file:
        yaml.dump(parsedreportfile, file)
