import requests
import json
from datetime import datetime

#this is the function to return the list of the notification_channel_ids present
def notification_channel_id(api_token,url):
    headers = {"Authorization": f'Bearer {api_token}'}
    response = requests.get(url, headers=headers)
    # print(response.json()["alerts"][0]["notificationChannelIds"])
    return response.json()["alerts"][0]["notificationChannelIds"] 

#This is the function to create the silencing
def silencing_alert(curr_time_in_millisec,json_data):

    for dict in json_data:
        api_token=dict["api_token"]

        #This is the endpoint for the silencing
        url='https://'+dict['region'].split('_')[0].lower()+'-'+dict['region'].split('_')[1].lower()+'.monitoring.cloud.ibm.com/api/v1/silencingRules'

        #this is the endpoint for all the alerts present
        alert_url='https://'+dict['region'].split('_')[0].lower()+'-'+dict['region'].split('_')[1].lower()+'.monitoring.cloud.ibm.com/api/alerts'
        # print(url)
        # print(api_token)
        silence_config = {
            "durationInSec": dict["duration_in_hours"]*60*60,
            "enabled":True,
            "name": f'Silencing the Cluster with name: {dict["cluster_name"]}',
            "notificationChannelIds": notification_channel_id(api_token,alert_url),
            # "scope": "kubernetes.cluster.name in (\"webapCluster/cfvdf6ef0lb6gpb1puig\")",
            "scope":f'kubernetes.cluster.name in (\"{dict["cluster_name"]}\")',
            "startTs": curr_time_in_millisec
        }

        headers = {'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(silence_config))

        if response.status_code == 201:
            silence_id = response.json()['id']
            print(f'Silencing rule created successfully with ID:{silence_id}')
        else:
            error_message = response.json()['errors'][0]['message']
            print(f'Error creating alert: {error_message}')


def main():

    
    #to fetch the current date and time 
    now=datetime.now()
    curr_time_in_millisec = now.timestamp() * 1000

    #converting the json file into python objects
    json_file=open('template.json','r')
    json_data = json.load(json_file)

    silencing_alert(curr_time_in_millisec,json_data)
    
if __name__=='__main__':
    main()


