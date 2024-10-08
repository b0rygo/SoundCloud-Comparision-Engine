import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import difflib
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

def utwory_z_folderu(dis): #FUNCTION THAT SHOWS YOUR SONGS FROM FOLDER
    try:
        if not os.path.isdir(dis):
            print(f"Ścieżka {dis} nie jest katalogiem.") # IT MEANS THAT THE PATH IS NOT A DIRECTORY
            return []
        pliki = os.listdir(dis)
        pliki_bez_mp3 = [os.path.splitext(plik)[0].lower() for plik in pliki]  # EVERYTHING IS LOWER FONT AND SAVED INTO ARRAY
        pliki_bez_mp3.sort()  # SORTING LIST
        print(f"Pliki w katalogu '{dis}': {pliki_bez_mp3}")
        return pliki_bez_mp3

    except Exception as e:
        print(f"Wystąpił błąd: {e}") # COM ABOUT ERROR
        return []

def utwory_z_soundclouda(playlist_url): #FUNCTION THAT SHOWS YOUR SONGS FROM SC
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(playlist_url)
        time.sleep(10)  # WAITING FOR THE SITE 10SEC

        # USING WEBDRIVER
        track_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "trackItem__trackTitle"))
        )

        titles = [element.text.lower() for element in track_elements]  # ELEMENTS IN ARRAY TO LOWER FONT VERSION
        driver.quit()  # CLOSING BROWSER
        return titles

    except Exception as e:
        print(f"Wystąpił błąd: {e}") # COM ABOUT ERROR
        return []

def znajdz_podobne(tytul, lista):
    wyniki = difflib.get_close_matches(tytul, lista, n=1, cutoff=0.6)
    if wyniki:
        return wyniki[0]
    else:
        return None

dis = 'D:\\HARDTECHNOJAKCHUJ' # DIRECTORY PATH
playlist_url = 'https://on.soundcloud.com/4m9pzRz1mp42gCFr5' #LINK TO YOU PUBLIC PLAYLIST AT SOUNDCLOUD
folder_songs = utwory_z_folderu(dis)
soundcloud_songs = utwory_z_soundclouda(playlist_url)

niepasujace_piosenki = [] #ARRAY TO SONGS THAT ARE NOT IN YOUR FOLDER

for soundcloud_title in soundcloud_songs:
    dopasowanie = znajdz_podobne(soundcloud_title, folder_songs)
    if dopasowanie is None:
        niepasujace_piosenki.append(soundcloud_title) # ADDING TO ARRAY SONGS THAT ARE NOT IN YOUR PLAYLIST

# SHOWING YOUR MISSING SONGS
if niepasujace_piosenki:
    print("Brakujące piosenki:")
    for i, song in enumerate(niepasujace_piosenki, start=1):
        print(f"{i}. {song}")
else:
    print("Nie znaleziono brakujących piosenek.")

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(1200,300,500,500)
    win.setWindowTitle("SoundCloud-Comparision-Engine")
    win.show()
    sys.exit(app.exec_())