import cv2
import os

# ========================== USER SETTINGS ===========================

# haarcascade_frontalface_default.xml 경로
HAAR_CASCADE_PATH = ""

# ========================== DON'T EDIT ==============================

def camera(cam):
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    
    # 라즈베리파이에서 카메라로 이미지 촬영 (sample.jpg 저장)
    terminal_command = "libcamera-jpeg -o sample.jpg --camera %d -t 5000" % cam
    os.system(terminal_command)

    # 이미지 읽고 흑백 변환 후 얼굴 인식
    image = cv2.imread('/home/pi/smart_elevator/sample.jpg')
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImage, 1.2, 7)

    # 촬영한 이미지 삭제
    os.system("rm sample.jpg")

    return len(faces)
