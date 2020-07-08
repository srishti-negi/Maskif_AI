import cv2
import argparse
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
ds_factor = 0.5

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release(0)
    """
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode(".jpg", image)
        data = jpeg.tobytes()
        return data
    """
    
    def get_frame(self):
        frame_status, frame = self.video.read()
        frame = cv2.resize(frame,None, fx = ds_factor, fy = ds_factor, interpolation = cv2.INTER_AREA)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        wearing_mask = None
        for (x, y, w, h) in faces:
            """
            descaled_x = int(x/ds_factor)
            descaled_y = int(y/ds_factor)
            descaled_w = int(w/ds_factor)
            descaled_h = int(h/ds_factor)
            """
            #ROI = Region of interest
            face_frame = frame[y : y + h, x : x + w]
            
            """
            center = (x + w//2, y + h//2)
            frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            faceROI = frame_gray[y:y+h,x:x+w]
            """
            faceROI = frame_gray[y:y+h,x:x+w]
            #face_frame = frame[descaled_y:descaled_+descaledH, descaledX:descaledX+descaledW]
            
            resized_frame = cv2.resize(face_frame, (256, 256))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            """
            roi_gray_mouth = gray_frame[y+(int(h/2)):y+h, x:x+w]
            roi_mouth = frame[y+(int(h/2)):y+h, x:x+w]

            roi_gray_eye = gray_frame[y-(int(h/2)):y+h, x:x+w]
            roi_eye = frame[y-(int(h/2)):y+h, x:x+w]
            """
        
            eyes = eye_cascade.detectMultiScale(faceROI, 1.05, 100)
            mouth = mouth_cascade.detectMultiScale(faceROI, 1.05, 200)
            nose = nose_cascade.detectMultiScale(faceROI, 1.3, 5)

            #eye circles
            for (x2,y2,w2,h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                frame = cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
            #mouth rect
            for (ex,ey,ew,eh) in mouth:
                frame = cv2.rectangle(frame,(x + ex,y + ey),(x + ex+ew,y + ey+eh),(0,0,255),3)

            #nose
            for (nx,ny,nw,nh) in nose:
                frame =  cv2.rectangle(frame, (x + nx,y + ny), (x + nx+nw,y + ny+nh), (0,255,0), 3)
                #break

            #print(no_of_eyes, no_of_mouths)

            no_of_eyes = len(eyes)
            no_of_mouths = len(mouth)
            no_of_noses = len(nose)
            """
            if no_of_eyes >= 1 and no_of_mouths == 0 and no_of_noses == 0:
                wearing_mask = True
            if no_of_eyes >= 1 and (no_of_mouths >= 1 or no_of_noses >= 1):
                wearing_mask = False

            """
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
            #frame = cv2.rectangle(frame, (x, y), (x + w, y + h), frame_color, 3)
            face_label = "Wearing mask: " + str(wearing_mask)

            frame = cv2.putText(frame, face_label, (x - w, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (255, 0, 0) )
            break
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()


     
"""
    def get_frame(self):
        success, image = self.video.read()
        image = cv2.resize(image, None, fx = ds_factor, fy = ds_factor, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.05, 100)
        for (x, y, w, h) in face_rects:
#            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            descaledX = int(x/ds_factor)
            descaledY = int(y/ds_factor)
            descaledW = int(w/ds_factor)
            descaledH = int(h/ds_factor)

            #resized_frame = cv2.resize(image, (256, 256))
            
#            face_frame = image[y+y+h, x:x+w]
            face_frame = image[descaledY:descaledY+descaledH, descaledX:descaledX+descaledW]
            
            resized_frame = cv2.resize(face_frame, (256, 256))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
           
            no_of_eyes = len(eye_cascade.detectMultiScale(gray_frame, 1.05, 100))
            no_of_mouths = len(mouth_cascade.detectMultiScale(gray_frame, 1.05, 200))
            print(no_of_eyes, no_of_mouths)
            wearing_mask = None
            if no_of_eyes >= 2 and no_of_mouths == 0:
                wearing_mask = True
            elif no_of_eyes >= 2 and no_of_mouths >= 1:
                wearing_mask = False
            
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 3)
            #image = cv2.rectangle(image, (descaledX, descaledY), (descaledX+descaledW, descaledY+descaledH), (255, 0, 0), 3)
            face_label = "Wearing mask: " + str(wearing_mask)
            image = cv2.putText(image, face_label, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (255, 0, 0))
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
"""


    
