import requests
import speech_recognition as sr
import pyaudio
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


r = sr.Recognizer()

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("I didn't get that")
        except sr.RequestError:
            print("Sorry, the service is down")
        print(f">> {voice_data.lower()}")
        return voice_data.lower()
    
def get_url(search_term):
    template = 'https://www.tokopedia.com/search?st=product&q={}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
    search_term = search_term.replace(' ', '%20')
    return template.format(search_term)

def respond(voice_data):
    if "i want to buy something" in voice_data:
        search = record_audio("What do you want to buy for?")
        url = get_url(search)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        jdl = []
        prc = []
        
        for judul in soup.find_all("div", class_="css-1b6t4dn", ):
            temp1 = judul.get_text()
            jdl.append(temp1)
        for angka in soup.find_all("div", class_="css-1ksb19c", ):
            temp2 = angka.get_text()
            prc.append(temp2)
        
        print("here are the prices \n")
        for i in range (0, 10):
            print(jdl[i])
            print(prc[i] + "\n")

voice_data = record_audio
respond(voice_data())