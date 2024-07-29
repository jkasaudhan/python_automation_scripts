import pyttsx3
import requests

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def trndnews():
    url = " http://newsapi.org/v2/top-headlines?country=us&apiKey=GET_YOUR_OWN"
    page = requests.get(url).json()
    article = page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])
    for i in range(len(results)):
        print(i + 1, results[i])
    speak(results)


trndnews()

''' Run The Script To Get The Top Headlines From USA'''
