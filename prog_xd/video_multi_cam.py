# trouver l'IP des ESP-CAM et afficher leurs videos
from video_search import *
import numpy as np
import cv2

def video_capture(dic_ip_cam):
    liste_video_capture = []
    nom_cam = []
    for ip,num in dic_ip_cam.items():
        #print("ip,num: ",ip,num)
        url = f"http://{ip}/live"
        liste_video_capture.append(cv2.VideoCapture(url)) #video_capture_0 = cv2.VideoCapture('http://192.168.1.65/live')
        nom_cam.append(num)
        #print("liste_video_capture: ",liste_video_capture)
    return liste_video_capture,nom_cam

def display(liste_video_capture, nom_cam):
    while True:
        for i in range(len(liste_video_capture)):
            ret,frame = liste_video_capture[i].read() #ret0, frame0 = video_capture_0.read()
            cv2.imshow(nom_cam[i], frame) #     cv2.imshow('Cam 0', frame0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    my_ip = get_ip_address()
    my_netmask = get_netmask_address(my_ip)
    n = get_IP_min_max(my_ip,my_netmask) #fabrique les ip du reseau
    dic_ip_cam = cherche_ip_cam(n) #recherche les caméras dans ce reseau
    print("touche q pour sortir de l'application")
    liste_video_capture,nom_cam = video_capture(dic_ip_cam)
    display(liste_video_capture,nom_cam)
    
# When everything is done, release the capture
for vc in liste_video_capture:
    vc.release()
cv2.destroyAllWindows()