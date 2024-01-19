import requests
import json
import pandas as pd
import os 

# You Input 
username = "{}"
password = "{}"
path_file= "{}" # save location 


#################################################
              #Step 1: Access
##################################################


url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": username,
  "password": password
})
headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic Og=='
}

response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)
User_Profile_df = json.loads(response.text)


#################################################
              #Step 2: Identify SessionId
##################################################

df = pd.json_normalize(User_Profile_df)

sessionId = df['sessionId'].iloc[0]

#################################################
              #Step 3: Pull securityLog     ### query via time frame
##################################################

# Reference: https://docs.informatica.com/integration-cloud/b2b-gateway/current-version/rest-api-reference/platform-rest-api-version-3-resources/security-logs.html

url = "https://nac1.dm-na.informaticacloud.com/saas/public/core/v3/securityLog"

#query = "?q=entryTime>='2023-09-28T08:00:00.000Z';entryTime<='2023-10-03T17:00:00.000Z'

#For Data Integration, use one of the following codes: v2/task?type=MTT
# DMASK. Masking task.
# DRS. Replication task.
# DSS. Synchronization task.
# MTT. Mapping task.
# PCS. PowerCenter task.

payload = {}
headers = {
  'INFA-SESSION-ID': sessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}

response = requests.request("GET", url, headers=headers)

securityLog = json.loads(response.text)
securityLog_df = pd.json_normalize(securityLog, record_path='entries')

userid = os.getlogin()
file_path = "{file_path}"

writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
securityLog_df.to_excel(writer, sheet_name='BulkEntities', index=False)
writer.close()

#################################################
              #Step 4: Pull auditLog     ### query via time frame
##################################################
import requests
import json

url = "https://nac1.dm-na.informaticacloud.com/saas/api/v2/auditlog"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': sessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


auditlog = json.loads(response.text)
auditlog_df = pd.json_normalize(auditlog)

userid = os.getlogin()
file_path = file_path

writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
auditlog_df.to_excel(writer, sheet_name='BulkEntities', index=False)
writer.close()










