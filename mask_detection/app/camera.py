import cv2
import argparse

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
ds_factor = 0.5

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release(0)
    
    def get_frame(self):
        frame_status, frame = self.video.read()
        frame = cv2.resize(frame,None, fx = ds_factor, fy = ds_factor, interpolation = cv2.INTER_AREA)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.equalizeHist(gray_frame)
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        wearing_mask = None
        for (x, y, w, h) in faces:
            face_frame = frame[y : y + h, x : x + w]
            resized_frame = cv2.resize(face_frame, (256, 256))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            
            nose = nose_cascade.detectMultiScale(face_frame, 1.3, 5)
            
            for (nx,ny,nw,nh) in nose:
                frame =  cv2.rectangle(frame, (x + nx,y + ny), (x + nx+nw,y + ny+nh), (0,255,0), 3)
    
            no_of_noses = len(nose)
            if no_of_noses == 0:
                wearing_mask = True
            else:
                wearing_mask = False
            
            if wearing_mask == True:
                frame_color = (0, 255, 0)
            elif wearing_mask == False:
                frame_color = (0, 0, 255)
            else:
                frame_color = (255, 0, 0)
            center = (x + w//2, y + h//2)

            frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, frame_color, 4)
            face_label = "Wearing mask: " + str(wearing_mask)

            frame = cv2.putText(frame, face_label, (x - w, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (255, 0, 0) )
            break
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes(), wearing_mask