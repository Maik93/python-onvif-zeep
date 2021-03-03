import cv2
import os
import sys
import yaml

# References:
# https://carlrowan.wordpress.com/2018/12/23/ip-camera-control-using-python-via-onvif-for-opencv-image-processing/
# https://www.ispyconnect.com/man.aspx?n=Reolink model RLC-423

script_path = os.path.dirname(sys.argv[0])
with open(os.path.join(script_path, "credentials.yaml")) as f:
    credentials = yaml.full_load(f)
    IP = credentials['ip']
    USER = credentials['user']
    PASS = credentials['password']
    STREAMING_URI = credentials['streaming_uri']

camera_url = f"rtsp://{USER}:{PASS}@{IP}/{STREAMING_URI}"

video_capture = cv2.VideoCapture(camera_url)

while True:
    is_ok, frame = video_capture.read()
    if is_ok:
        cv2.imshow('frame', frame)
    else:
        print("no video!")
    if cv2.waitKey(1) == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
