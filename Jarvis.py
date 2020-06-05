import pyttsx3  # module to convert text to speech
import datetime  # module to give current date and time
import speech_recognition as sr  # module to take input from microphone as query
import wikipedia  # module to interact with searching on wikipedia
import smtplib  # module to import SMTP client
from selenium import webdriver  # module to access particular web browser
from selenium.webdriver.common.keys import Keys  # module to access keys
import os  # module provides functions for interacting with operating systems
import pyautogui  # module to interact with GUI (here, for screenshot)
import psutil  # module to retrieve information of OS (like memory usage, CPU usage etc)
import pyjokes  # module imports one liner jokes

engine = pyttsx3.init()  # initialize pyttsx3 drivers
engine.setProperty('rate', 150)  # speed percent (can go over 100)
engine.setProperty('volume', 1.0)  # volume 0-1

# speak function
def speak(audio):
    engine.say(audio)  # queue a command to speak an utterance
    engine.runAndWait()  # returns when all commands queued before this call are emptied from the queue

# time function
def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")  # formatting string as (hr:min:sec)
    speak("Current Time is:")
    speak(Time)

# time function
def date():
    year = int(datetime.datetime.now().year)  # returns year
    month = int(datetime.datetime.now().month)  # returns month
    date = int(datetime.datetime.now().day)  # returns date
    speak("Current Date is:")
    speak(date)  # -----
    speak(month)  # |------- this is for utterance to have in a specific format
    speak(year)  # -----

# wishme function [this function will make jarvis greet you on your welcome]
def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:  # if its 6am and less than 12pm it will greet good morning
        speak("Good Morning,Sir!. Welcome!")
    elif hour >= 12 and hour < 17:  # if its 12pm and less than 5pm it will greet good afternoon
        speak("Good Afternoon,Sir!. Welcome!")
    elif hour >= 17 and hour < 24:  # if its 5pm and less than 12am it will greet good evening
        speak("Good Evening,Sir!. Welcome!")
    else:
        speak("Good Night Sir!")  # if its 12am and less than 6am it will greet good night
    time()
    date()
    speak("Jarvis at your service. How can I help you?")

# takeCommand function [takes input from user]
def takeCommand():
    r = sr.Recognizer()  # accessing sr module method called Recognizer
    with sr.Microphone() as source:  # use the default microphone as the audio source
        print("Listening.......")
        r.pause_threshold = 1  # 1 second pause for proper execution
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
    try:
        print("Recognizing.......")
        query = r.recognize_google(audio, language='en-in')  # uses google speech API
        print(query)
    except Exception as e:
        print(e)
        speak("Can't here you. Say that again!")
        return "None"
    return query  # returns query

# sendEmail function
def sendEmail(to, content):  # passed 2 arguments (to & content)
    server = smtplib.SMTP('smtp.gmail.com', 587)  # accessed SMTP client server of gmail with port
    server.ehlo()  # verify and connects to ESMTP sever
    server.starttls()  # connects to TLS[transport layer security - Provides Encryption]
    server.login('Email ID', 'Password') # login to server with username and password
    server.sendmail('Email ID', to, content) # sends email from designated email id

# screenshot function
def screenshot():
    img = pyautogui.screenshot()   # access screenshot method from pyautogui module
    img.save(r"")  # address to save screenshot on your device

# cpu usage function
def cpu():
    usage = str(psutil.cpu_percent()*10)  # converts the output to string
    speak("CPU is at" + usage)
    print(usage)

# joke function
def jokes():
    speak(pyjokes.get_joke())   # get jokes from  pyjokes module


if __name__ == "__main__":
    wishme() # function call for wishme function
    while True:
        query = takeCommand().lower()  # makes input lowercase
        if 'time' in query:
            time()  # function call for time function

        elif 'date' in query:
            date()   # function call for date function

        elif 'wikipedia' in query:
            speak("Searching.......")
            query = query.replace("wikipedia", "")  # replace wikipdedia with blank string in query
            result = wikipedia.summary(query, sentences=2)  # gives summary of input upto 2 sentences
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What message you want to deliver?")
                content = takeCommand()   # message body
                to = 'recipient Email ID'   # whom you want to send email
                sendEmail(to,content)   # sends email
                print(to)
                print(content)
                speak("Email sent Successfully.")
            except Exception as e:
                print(e)
                speak("Unable to send email.")

        elif 'search in chrome' in query:
            speak("what should I Search?")
            search = takeCommand().lower()   # makes input lowercase
            bot = webdriver.Chrome(r"")  # device address where chromedriver is present
            bot.get('https://www.google.com/')
            result = bot.find_element_by_name('q')  # this will give value of name in line HTML of web browser
            result.clear() # clear field if anything written
            result.send_keys(search) # send keys to searchbox
            result.send_keys(Keys.RETURN)  # return keys

        elif 'play songs' in query:
            songs_dir = '' # device address where songs directory is present
            songs = os.listdir(songs_dir) # returns list of song directory
            os.startfile(os.path.join(songs_dir, songs[0]))  # joins with song directory, then plays first song of directory

        elif 'remember that' in query:
            speak("What should I remember?")
            data = takeCommand()
            speak("you said me to remember" + data)
            remember = open('data.txt', 'w')  # opens the file in write mode
            remember.write(data)  # writes data in the file
            remember.close()  # closes the file

        elif 'do you remember anything' in query:
            remember = open('data.txt', 'r')  # opens the file in read mode
            speak("you said me to remember that" + remember.read())

        elif 'screenshot' in query:
            screenshot()  # function call of screenshot
            speak("screenshot taken successfully")

        elif 'cpu' in query:
            cpu()  # function call of cpu

        elif 'joke' in query:
            jokes() # function call of joke

        elif 'offline' in query:
            quit()  # shutdowns the program
