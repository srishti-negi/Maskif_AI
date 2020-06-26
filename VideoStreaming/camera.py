import cv2

#face_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")
ds_factor = 0.7

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.resize(image, None, fx = ds_factor, fy = ds_factor, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
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
           
            no_of_eyes = len(eye_cascade.detectMultiScale(gray_frame, 1.1, 2))
            no_of_mouths = len(mouth_cascade.detectMultiScale(gray_frame, 1.9, 2))
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

