import cv2
import streamlit as st
import numpy as np
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




# URL du flux vidéo
url = "http://172.17.113.243/live"

# Ouvrir le flux vidéo avec OpenCV
cap = cv2.VideoCapture(url)

# Vérifier si le flux vidéo est ouvert
if not cap.isOpened():
    st.error("Erreur d'ouverture du flux vidéo")

# Récupérer les dimensions du flux vidéo
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Configuration Streamlit
st.title("Reconstruction de la vidéo en direct")
video_placeholder = st.empty()


# Liste pour stocker les frames
frames = []

# Boucle principale pour capturer et afficher les frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.error("Erreur de lecture du flux vidéo")
        break

    # Stocker la frame dans la liste
    frames.append(frame)

    # Afficher l'image dans la fenêtre Streamlit
    video_placeholder.image(frame, channels="BGR")

# Afficher la vidéo reconstituée
if st.button("Afficher la vidéo"):
    st.video(np.array(frames))




