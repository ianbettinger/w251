import paho.mqtt.client as mqtt

local_broker = "172.18.0.2"
remote_broker = "169.62.76.2"
topic = "tx2/face"

def on_connect_local(client,userdata,flags,rc):
    print("connected to local mqtt")
    x=client.subscribe(topic)
    print(x)
    print("test subscrib",result)

def on_connect_remote (client, userdata,flags,rc):
    print("connected to remote broker with rc:" + str(rc))

def on_message (client,userdata,msg):
    print(msg.topic+" "+"you got to message")# str(msg.payload
    remote_client.publish(topic,payload=msg.payload,qos=1,reta

local_client=mqtt.Client("forwarder")
local_client.on_connect=on_connect_local
local_client.connect(local_broker)
local_client.on_message=on_message

local_client=mqtt.Client("forwarder")                         
local_client.on_connect=on_connect_local                      
local_client.connect(local_broer)                            
local_client.on_message=on_message                            
                                                              
remote_client=mqtt.Client("forwarder")  
remote_client.on_connect=on_connect_remote
remote_client.connect(remote_broker)      
                                          
local_client.loop_forever()               
                                