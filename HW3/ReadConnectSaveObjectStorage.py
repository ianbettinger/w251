import ibm_boto3
import pandas as pd
import io

import numpy as np
import cv2
import math

import paho.mqtt.client as mqtt

# connect to IBM Cloud Object Storage
bucket_name = 'tx2'
#filename = '2015-death-data-v2.csv'

##Credentials
credentials = {
          "apikey": "",
            "cos_hmac_keys": {
                    "access_key_id": "",
                        "secret_access_key": ""
                          },
              "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
                "iam_apikey_description": "Auto-generated for key ",
                  "iam_apikey_name": "Service credentials-1",
                    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                      "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity:",
                        "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:"
                        }

###Connect to server
from ibm_botocore.client import Config
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us-south.cloud-object-storage.appdomain.cloud'#'https://s3-api.us-geo.objectstorage.softlayer.net'

resource = ibm_boto3.resource('s3',
                              ibm_api_key_id=credentials['apikey'],
                                                    ibm_service_instance_id=credentials['resource_instance_id'],
                                                                          ibm_auth_endpoint=auth_endpoint,
                                                                                                config=Config(signature_version='oauth'),
                                                                                                                      endpoint_url=service_endpoint)

import urllib

#csv_url = 'https://projects.fivethirtyeight.com/nba-model/nba_elo.csv'
#csv_name = '1Test-safety'

from datetime import datetime

MQTT_HOST = "169.62.76.2"
MQTT_PORT = 1883
MQTT_TOPIC = "tx2/face"

def on_connect (client, userdata,flags,rc):
    print("connected to local cloud broker with rc:" + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client,userdata,msg):
    print("in message function")
    now=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print("date and time:",now)
    img_name = "face-" + now + ".png"
    print("imagename",img_name)
    resource.Bucket(name=bucket_name).put_object(Key=img_name, Body=msg.payload)
    print("put in bucket")

mqttclient=mqtt.Client()
mqttclient.on_connect=on_connect
mqttclient.connect(MQTT_HOST,MQTT_PORT, 60)
mqttclient.on_message = on_message

mqttclient.loop_forever()



