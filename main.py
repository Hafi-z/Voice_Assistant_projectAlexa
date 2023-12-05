import datetime
import subprocess
import playsound
import pyjokes
import wikipedia
import speech_recognition as sr
import pyttsx3
import pywhatkit
import smtplib
import requests
import webbrowser as wb
from gtts import gTTS
from bs4 import BeautifulSoup
from email.message import EmailMessage
from translate import Translator

translator = Translator(to_lang="bn")
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# get all the voice information
# for v in voices:
#     print(v)
engine.setProperty('voice', 'com.apple.voice.compact.en-US.Samantha')

email_list = {
    'hafiz edu': 'hafizur1113@student.nstu.edu.bd',

    'hafiz': 'hafiz.ishrak2@gmail.com'
}

browse_sites = {
    'nstu': 'https://www.nstu.edu.bd/',
    'codeforces': 'https://codeforces.com/',
    'usaco guide': 'https://usaco.guide/',
    'codechef': 'https://www.codechef.com/',
    'atcoder': 'https://atcoder.jp/',
    'messenger': 'https://www.messenger.com/',
    'bbc news': 'https://www.bbc.com/news',
    'facebook': 'https://www.facebook.com/',
    'google': 'https://www.google.com/',
    'youtube': 'https://www.youtube.com/',
    'twitter': 'https://twitter.com/login',
    'discord': 'https://discord.com/',
    'gmail': 'https://mail.google.com/mail/',
}

app_list = {
    'code blocks': 'C:\\Program Files\\CodeBlocks\\codeblocks.exe',
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'pycharm': 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2022.2.1\\bin\\pycharm64.exe',
    'word': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
    'excel': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
    'powerpoint': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
    'whatsapp': 'C:\\Users\\User\\AppData\\Local\\WhatsApp\\WhatsApp.exe',
    'notepad': 'C:\\WINDOWS\\system32\\notepad.exe',
    'snipping tool': 'C:\\WINDOWS\\system32\\SnippingTool.exe',
}

def talk(text):
    print('inside talk(text)')
    engine.say(text)
    engine.runAndWait()
def take_command():
    command = 'turn off'
    try:
        print('try, not exception')
        with sr.Microphone() as source:
            talk('listening')
            print('listening...')
            listener.adjust_for_ambient_noise(source,duration=1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)

            #command = listener.recognize_google(voice,language='bn-BD')    #to take speech as text from other languages than english.

            command = command.lower()
            command = command.replace('alexa', '')

            #For hearing texts in other languages from assistant we can use following commented lines of code..
            #talk(command)
            #command = gTTS(text=command, lang='bn', slow=False)
            #command.save("command.mp3")
            #playsound.playsound("command.mp3", True)
    except:
        print('exception')
        pass
    return command

def get_info():
    try:
        with sr.Microphone() as source:
            print('listening..')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
    except:
        pass
    return command

def run_alexa():
    command = take_command()
    print('user: ' + command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        print('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif 'temperature' in command:
        try:
            talk("in which location?")
            print("assistant: in which location?")
            location = get_info()
            print('user: '+location)
            search = 'temperature in '+location
            url = "https://www.google.com/search?q="+search
            r = requests.get(url)
            data = BeautifulSoup(r.content, "html.parser")
            temp = data.find("div",attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
            temp =temp[0]+temp[1]+"° celsius"
            talk(f"current {search} is {temp}")
            print(f"assistant: current {search} is {temp}")
        except:
            pass
    elif 'send email' in command:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('hafiz.ishrak1@gmail.com', 'biubnftflxiicnkj')     #app password should be given

        print('assistant: To whom you want to send email')
        talk('To whom you want to send email')
        receiver = get_info()
        print('user: ' + receiver)
        print('assistant: What is the subject of your email?')
        talk('What is the subject of your email?')
        subject = get_info()
        print('user: ' + subject)
        print('assistant: Tell me the text of your email')
        talk('Tell me the text of your email')
        message = get_info()
        print('user: ' + message)

        email = EmailMessage()
        email['From'] = 'hafiz.ishrak1@gmail.com'
        email['To'] = email_list[receiver]
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)
        print('assistant: Email sent successfully!')
    elif 'who' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person,1)
        print(info)
        talk(info)
    elif 'open in browser' in command:
        print('assistant: which website do you want to visit?')
        talk('which website do you want to visit?')
        address = get_info()
        print('user: '+address)
        wb.open(browse_sites[address])
    elif 'open app' in command:
        try:
            print('assistant: which app do you want to open?')
            talk('which app do you want to open?')
            app = get_info()
            print('user: '+app)
            subprocess.Popen(app_list[app])
        except:
            pass
    elif 'কয়টা বাজে' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        tm = gTTS(text=time, lang='bn', slow=False)
        tm.save("tm.mp3")
        playsound.playsound("tm.mp3", True)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'joke' in command:
        abc = pyjokes.get_joke()
        print(abc)
        talk(abc)
    elif 'translate' in command:
        tx=command.replace('translate', '')
        translated_txt = translator.translate(tx)
        print(translated_txt)
    elif 'turn off' in command:
        talk('goodbye sir')
        return 1
    else:
        talk('I didnt get that, sir!')
        talk('please say that again sir')
    return 0

while True:
    a = run_alexa()
    if a:
        break