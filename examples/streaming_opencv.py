import cv2

# References:
# https://carlrowan.wordpress.com/2018/12/23/ip-camera-control-using-python-via-onvif-for-opencv-image-processing/
# https://www.ispyconnect.com/man.aspx?n=Reolink model RLC-423

IP = "192.168.0.100"  # Camera IP address
USER = "admin"  # Username
PASS = "admin"  # Password

camera_url = f"rtsp://{USER}:{PASS}@{IP}/h264Preview_01_sub"
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
