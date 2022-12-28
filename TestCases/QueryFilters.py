#!/usr/lib/python3
import requests
import yaml

def QueryFilter(workdirectory,AuthToken,tenantid,portal,starttimeUNIX,endtimeUNIX,starttimenanosec,endtimenanosec) :


    reportfile = open(workdirectory + "/Report.yml")
    parsedreportfile = yaml.load(reportfile,Loader=yaml.FullLoader) 
    QueryFilter_FunctionalityList = parsedreportfile['QueryFilter_Functionality']
    
    payload={}
    headers = {
     'Authorization': AuthToken,
     'Content-Type': 'application/json'
    }

    labelsurl  = "https://"\
        +portal+\
        "/logsrql/api/v7/tenants/"\
        +tenantid+\
        "/logs/labels?start"\
        +str(starttimeUNIX)+\
        "&end="\
        +str(endtimeUNIX)

    labels_response = requests.request("GET", labelsurl, headers=headers, data=payload)
    if labels_response.status_code == 200 :
        labelsresponsejson = labels_response.json()
        labelsdata = labelsresponsejson['data']
            
        for i in labelsdata :
            
            valueurl = "https://"\
            +portal+\
            "/logsrql/api/v7/tenants/"\
            +tenantid+\
            "/logs/label/"\
            +i+\
            "/values?start"\
            +str(starttimeUNIX)+\
            "&end="\
            +str(endtimeUNIX)

            value_response = requests.request("GET", valueurl, headers=headers, data=payload)
            if value_response.status_code == 200:
                valuesresponsejson = value_response.json()
                valuesdata = valuesresponsejson['data']
                
                logsresultStatus=False
                stream = ""
                for k in valuesdata:
                    
                    logsurl = "https://"\
                        +portal+\
                        "/logsrql/api/v7/tenants/"\
                        +tenantid+\
                        "/logs?query={"\
                        +i+\
                        "="\
                        '"'\
                        +k+\
                        '"'\
                        "}&limit=51&start="\
                        +str(starttimenanosec)+\
                        "&end="\
                        +str(endtimenanosec)

                    log_response = requests.request("GET", logsurl, headers=headers, data=payload)
                    logsresponsejson = log_response.json()
                    logsdata = logsresponsejson['data']
                    logsresultdata = logsdata['result'] 
                    for p in logsresultdata:
                        stream = (p['stream'])           
                    if k in str(stream):
                        logsresultStatus=True    
                if not logsresultStatus:
                    status = "QueryFilter : " + i + " : Validation Fail - Logs are not coming for that Queryfilter\n"
                    QueryFilter_FunctionalityList.append(status)
                else:
                    status = "QueryFilter : " + i + " : Validation Pass - Logs are coming for that Queryfilter\n"
                    QueryFilter_FunctionalityList.append(status)
  
            else:
                status = value_response.reason
                QueryFilter_FunctionalityList.append(status)         
                
    else:
        status = labels_response.reason
        QueryFilter_FunctionalityList.append(status)       
        
    with open(workdirectory + "/Report.yml","w") as file :
        yaml.dump(parsedreportfile,file)
