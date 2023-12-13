import streamlit as st

import paho.mqtt.client as mqtt
import time

#-------configuration du broker------------
mqtt_broker = "pimqtt.local"
mqtt_port = 1883
mqtt_topic = "test/servo"

#-------config client-----
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

 #------fonction envoi de message-----------------   
def send_message(rap_cyc):
    message = str(rap_cyc)
    mqtt_client.publish(mqtt_topic, message)

#---------------------------------------------------
st.subheader("Commande du servomoteur ")
rotation = st.slider("angle de rotation",min_value=1,max_value=100,value=1,step=1)
angle=int(rotation*123//100)
send_message(angle)
mqtt_client.loop()
#-----------------------------------------------
