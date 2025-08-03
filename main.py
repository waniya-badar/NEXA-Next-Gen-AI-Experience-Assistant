import psutil
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyautogui
import sys
import time
import os
import json
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
from sklearn.preprocessing import LabelEncoder
import re


with open("intents.json") as file:
    data = json.load(file)

model = keras.models.load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices= engine.getProperty('voices') #0 = male voice and 1 = female voice
    engine.setProperty('voice',voices[1].id) #giving female id to the engine
    rate =engine.getProperty('rate')
    engine.setProperty('rate',rate-50)
    volume =engine.getProperty('volume')
    engine.setProperty('volume',volume+0.25)
    return engine
    
def speak(text):
    engine =initialize_engine()
    engine.say(text)
    engine.runAndWait()
    
# speak("hello , my name is waniya")

def command():
    r=sr.Recognizer() # to recognise voice from microphoe
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source ,duration=0.5) #for adjusting the outdoor or ambigious noise from micro
        print ("Listening ...",end="", flush=True) #automatically removes Listening...
        r.pause_threshold=1.0 #will wait for 1 second , if we dont speak till 1 second it will consider that we have stopped and it is a sentence
        r.phrase_threshold=0.3 # minimum length of a sentence to consider it phrase , other wise just yes or no 
        r.sample_rate = 48000 #sample hertz rate of mic
        r.dynamic_energy_threshold =True #alows to adjust dynamically
        r.operation_timeout=5 #if no speech within 5 sec , it consider it as a timeout
        r.non_speaking_duration=0.5  #duration of silence that is acceptable to take a break
        r.dynamic_energy_adjustment = 2 
        r.energy_threshold=4000 #how loud speech must be ?
        r.phrase_time_limit=10 # maximum a phrase can be 10 sec long
        #print(sr.Microphone.list_microphone_names())
        audio= r.listen(source)
    try:  
       print ("\r",end="", flush=True)  
       print ("Recongnizing speach ...",end="", flush=True) 
       query = r.recognize_google(audio , language = 'en-in')
       print ("\r",end="", flush=True)  
       print(f"User : {query}\n")
    except Exception as e:
        print("I beg you pardon , please say that again")
        return "None"
    return query

def cal_day():
    day=datetime.datetime.today().weekday() + 1 #returns 0 monday to 6 sunday therefore, we added +1 for 1:mon etc
    day_dict={
        1:"Monday", #added dict because weekday only gives number
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week=day_dict[day] #fetches day from dictionary using number
        print(day_of_week)
    return day_of_week

def wishMe():
    hour=int(datetime.datetime.now().hour)
    t=time.strftime("%I:%M:%p")
    day=cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Waniya, it's {day} and time is {t}")
    elif(hour>=12) and (hour<=16) and ('PM' in {t}):
        speak(f"Good afternoon Waniya, it's {day} and time is {t}")
    else:
        speak(f"Good evening, it's {day} and time is {t}")

def social_media(command):
    if 'facebook' in query:
        speak("opening your facebook")
        webbrowser.open("https://facebook.com/")
    elif 'whatsapp' in query:
        speak("opening your whatsapp")
        webbrowser.open("https://whatsapp.com/")
    elif 'discord' in query:
        speak("opening your discord")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in query:
        speak("opening your instagram")
        webbrowser.open("https://instagram.com/")
    elif 'chatgpt' in query:
        speak("opening your chatgpt")
        webbrowser.open("https://chatgpt.com/")
    elif 'linkedin' in query:
        speak("opening your linkedin")
        webbrowser.open("https://linkedin.com/")
    elif 'github' in query:
        speak("opening your github")
        webbrowser.open("https://github.com/")  
    elif 'wikipedia' in query:
        speak("opening your wikipedia")
        webbrowser.open("https://www.wikipedia.org/") 
    else:
        speak("no results found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.system('start mspaint')
    elif "vscode" in command or "visual studio code" in command:
        speak("opening Visual Studio Code")
        os.startfile(r'D:\Microsoft VS Code\Microsoft VS Code\Code.exe')
    elif "zoom" in command:
        speak("opening Zoom")
        os.startfile(r'C:\Users\Hp\AppData\Roaming\Zoom\bin\Zoom.exe')

def closeApp(command):
    if "calculator" in command:
        speak("Closing calculator")
        os.system('powershell "Get-Process | Where-Object {$_.MainWindowTitle -match \'Calculator\'} | Stop-Process -Force"')
    elif "notepad" in command:
        speak("Closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("Closing Paint")
        os.system('taskkill /f /im mspaint.exe')
    elif "vscode" in command or "visual studio code" in command:
        speak("Closing Visual Studio Code")
        os.system('taskkill /f /im Code.exe')
    elif "zoom" in command:
        speak("Closing Zoom")
        os.system('taskkill /f /im Zoom.exe')
    else:
        speak("Sorry, I couldn't find that application.")

def solve_math(query):
    query = query.lower()

    # Replace words with symbols
    query = query.replace("plus", "+")
    query = query.replace("add", "+")
    query = query.replace("minus", "-")
    query = query.replace("subtract", "-")
    query = query.replace("times", "*")
    query = query.replace("multiply", "*")
    query = query.replace("multiplied", "*")
    query = query.replace("into", "*")
    query = query.replace("divide", "/")
    query = query.replace("divided", "/")
    query = query.replace("mod", "%")
    query = query.replace("remainder", "%")

    # Extract the expression using regex
    expression = re.findall(r'[-+/*%]|\d+', query)

    if len(expression) < 3:
        return "Sorry, I couldn't understand the full expression."

    try:
        # Join as a proper string expression like "5+3"
        result = eval("".join(expression))
        return f"The answer is {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that."

def browsing(query):
    if 'google' in query:
        speak("Waniya, What should I search in google?")
        s=command()
        webbrowser.open(f"{s}")

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")


if __name__ == "__main__":
    wishMe()
    while True :
        query =command().lower()
        #query=input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query)  or ('chatgpt' in query) or ('linkedin' in query) or ('github' in query) or ('wikipedia' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif("volume up" in query) or ("increase volume" in query)or ("increase" in query):
            pyautogui.press("volumeup")
            speak("Volume is increased")
        elif("volume down" in query) or ("decrease volume" in query)or ("decrease" in query):
            pyautogui.press("volumedown")
            speak("Volume is decreased")
        elif("volume mute" in query) or ("mute the sound" in query)or ("mute" in query):
            pyautogui.press("volumemute")
            speak("Volume is muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query) or ("open vscode" in query) or ("open zoom" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query) or ("close vscode" in query) or ("close zoom" in query):
            closeApp(query)

        elif "exit" in query:
            sys.exit()
        elif ('plus' in query) or ('add' in query) or ('minus' in query) or ('subtract' in query) or ('divide' in query) or ('divided' in query) or ('times' in query) or ('multiply' in query) or ('multiplied' in query) or ('into' in query) or ('+' in query) or ('-' in query) or ('*' in query) or ('/' in query) or ('mod' in query) or ('remainder' in query) or ('calculate' in query):
            speak(solve_math(query))
        elif ("open google" in query) :
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        else:
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=50, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])[0]

            for intent in data['intents']:
                if intent['tag'] == tag:
                    response = random.choice(intent['responses'])
                    speak(response)
                    break

