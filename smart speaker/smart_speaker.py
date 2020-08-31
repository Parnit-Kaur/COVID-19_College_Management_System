import os
import time
import playsound
import speech_recognition as sr 
from gtts import gTTS
import requests

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
    speak("Please speak your roll number")
    rollno=get_audio()
    speak("Please speak your password")
    password=get_audio()
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


