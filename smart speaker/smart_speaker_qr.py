import os
import time
import playsound
import speech_recognition as sr 
from gtts import gTTS
import requests
import cv2
college_id=input("Please enter your College id: ")
print(college_id)


def speak(text):
    tts=gTTS(text=text, lang="en")
    filename="voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio= r.listen(source)
        said = ""

        try:
            said=r.recognize_google(audio)
            print(said.upper())
        except Exception as e:
            print("Exception: "+ str(e))

    return said.upper() 

text=get_audio()
if "HELLO" in text:
    speak("Welcome to COVID-19 college management system")
    speak("Please speak your Roll Number")  
    #speak("Please show the QRCode for your roll number")
    rollno=get_audio()
    #cap = cv2.VideoCapture(0)
    #detector = cv2.QRCodeDetector()
    #a=0
    #while a==0:
        #_, img = cap.read()
        #rollno, bbox, _ = detector.detectAndDecode(img)
        #if bbox is not None:
            #for i in range(len(bbox)):
                #cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            #if rollno:
                #print("QR Code detected, data:", rollno)
                #a=1 
        #cv2.imshow("img", img)    
        #if cv2.waitKey(1) == ord("q"):
            #break
    #cap.release()
    #cv2.destroyAllWindows()       
    
    speak("Please show the QR code for your password")
    # initalize the cam
    cap = cv2.VideoCapture(0)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    a=0
    while a==0:
        _, img = cap.read()
        # detect and decode
        password, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            # display the image with lines
            for i in range(len(bbox)):
            # draw all lines
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if password:
                print("QR Code detected, data:", password)
                a=1
            # display the result  
        cv2.imshow("img", img)    
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()        

    
    speak("Please speak your temperature")
    temperature=get_audio()
    speak("Thank you ")



API_KEY='parnit'    

url='http://127.0.0.1:5000/temperature'
API_ENDPOINT = "{}/{}/{}".format(url,college_id, rollno)
data1 = {'api_dev_key':API_KEY, 
        'api_option':'paste',
        'api_paste_format':'python'} 
data={
    'rollno':rollno,
    'password':password,
    'temperature':temperature
}        
r = requests.post(url = API_ENDPOINT, data = data) 
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 



