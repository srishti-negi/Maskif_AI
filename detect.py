import cv2
#import pkg_resources
#haar_xml = pkg_resources.resource_filename('cv2', 'data/haarcascade_frontalface_default.xml')
#img = cv2.imread('pic1.jpg')
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def classify(gray, img):    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
        roigray = gray[y:y+h, x:x+w]
        roicolor = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roigray, 1.1, 5)
        smiles = smile_cascade.detectMultiScale(roigray, 1.9, 20)
        a = len(eyes)
        b = len(smiles)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roicolor, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roicolor, (ex, ey), (ew+ex, ey+eh), (0, 255, 0), 2)
    try:
        return img, a, b
    except:
        return img, 0, 0

face_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/cv2/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/cv2/data/haarcascade_smile.xml')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)
while(1):
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = classify(gray, frame)[0]
    no_of_eyes = classify(gray, frame)[2]
    no_of_smiles = classify(gray, frame)[1]
    if no_of_eyes >= 2 and no_of_smiles > 0:
        cv2.putText(canvas, "MASK: FALSE", (100, 100),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    else:
        cv2.putText(canvas, "MASK: TRUE", (100, 100),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.imshow('image', canvas)
    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
