import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from Jarvis import speak

video = cv2.VideoCapture(0)

path = "D:\\Attendance Register"
images =[]
ClassNames = []
MyList= os.listdir(path)
print(MyList)
for cl in MyList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    ClassNames.append(os.path.splitext(cl)[0])
print(ClassNames)

def findEncodings(images):
    encodelist =[]
    for img in images:
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def markAttendance(name):
    with open('D:\\Opencv\\Attendance.csv', "a+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodelistknown = findEncodings(images)
print('Encode Complete')
speak("Encode Complete")

namefinallist = []

cap = cv2.VideoCapture(0)

while True:
    Success,img = cap.read()
    imgS= cv2.resize(img,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


    for EncodeFace,faceloc in zip (encodesCurFrame,facesCurFrame):
        MAtches = face_recognition.compare_faces(encodelistknown,EncodeFace)
        faceDis = face_recognition.face_distance(encodelistknown,EncodeFace)
        MatchIndex = np.argmin(faceDis)

        if MAtches[MatchIndex]:
            name = ClassNames[MatchIndex].upper()
            x = name[0].upper()
            y = name [1::].lower()
            name = x + y
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            if name not in namefinallist:
                namefinallist.append(name)
                print("The person has been identified as",name)
                markAttendance(name)
            


    cv2.imshow('Webcam',img)
    if cv2.waitKey(1) &0xff ==ord('q'):
        break
