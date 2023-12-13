import streamlit as st
import base64
import paho.mqtt.client as mqtt

#-------CONFIGURATION DE LA PAGE WEB-------------
st.set_page_config(
    page_title="SI - 2023",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
   
)
#----------fond d'écran-----------------
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("1002539.png")

#-------configuration du broker------------
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883


#-------config client-----
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

 #------fonction envoi de message-----------------   
def send_message(n,mqtt_topic):
    message = str(n)
    mqtt_client.publish(mqtt_topic, message)

#-----------------Injection CSS----------------------------------
with st.sidebar:
    st.image("nabs_man.jpg")
    st.image("robot.jpg")

st.title("PROJET SI 2023") 
st.subheader("ROBOT EXPLORER")
tilt = st.slider("tilt",min_value=1,max_value=100,value=50,step=1,key="1")
send_message(tilt,"robot/servo1")
pan = st.slider("pan",min_value=1,max_value=100,value=50,step=1,key="2")
send_message(pan,"robot/servo2")

init = st.button("initialisation de la position de la caméra")
st.subheader("DEPLACEMENT DU ROBOT")
col1, col2, col3 , col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
with col3 :
    mav = st.button(":arrow_up:")
col1, col2, col3 , col4, col5,col6, col7, col8, col9, col10 = st.columns(10)
with col1:
    pass
with col2:
    gau = st.button(":arrow_left:")
with col3:  
    stop = st.button(":black_square_for_stop:")
with col4:
    dte = st.button(":arrow_right:")
with col5:
    pass
with col3 :
    mar = st.button(":arrow_down:")


if init:
    send_message(50,"robot/servo1")
    send_message(50,"robot/servo2")
#------------MARCHE AVANT ET MARCHE ARRIERE-------------    
if mav:
    send_message(1023,"robot/mav")
if mar:
    send_message(1023,"robot/mar")
#----------DIRECTION----------------
if gau:
    send_message(256,"robot/gau")
if dte:
    send_message(256,"robot/dte")
#---------ARRET-------------
if stop:
    send_message(0,"robot/stop")


#------------BOUCLE MQTT----------
mqtt_client.loop()
#-----------------------------------------------
