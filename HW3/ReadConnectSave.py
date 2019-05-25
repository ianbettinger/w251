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
          "apikey": "jsOpqtiX8pFAqYU9wYmiysJIxb8UC3dDl8Z3ggNOGn96",
            "cos_hmac_keys": {
                    "access_key_id": "4caf20ec11824b9abd4d5aa2a0e53c2b",
                        "secret_access_key": "bd7ba469bba1e5e1f30f8f99c79f01dfa615626cc88749c9"
                          },
              "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
                "iam_apikey_description": "Auto-generated for key 4caf20ec-1182-4b9a-bd4d-5aa2a0e53c2b",
                  "iam_apikey_name": "Service credentials-1",
                    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                      "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/6e9283cbce194b1eb4b9bcb63e245cd7::serviceid:ServiceId-62ed5c30-841d-
46d9-a231-9abf131fd17c",
                        "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/6e9283cbce194b1eb4b9bcb63e245cd7:f4aa9824-e925-4e
91-9a5c-1c4c94123f0d::"
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



