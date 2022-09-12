import instaloader
import PySimpleGUI as sg
import datetime
from itertools import dropwhile, takewhile
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException

UNTILSEC = datetime.datetime.now()
d = datetime.timedelta(days=7)
SINCESEC = UNTILSEC - d
UNTIL = UNTILSEC
SINCE = SINCESEC
sg.theme('DarkGrey5')
layout = [
    [sg.Text('InstaSalker', font=('Any 70'), pad=(10, 10))],
    [sg.Text('Kullanıcı Adı Girin', size=(20, 1)), sg.InputText()],
    [sg.Text('Şifre Girin', size=(20, 1)), sg.InputText()],
    [sg.Text('Hedef Kullanıcı Adı Girin' ,size=(20, 1) ), sg.InputText()],
    [[sg.Text("Text Dosyasını Seç: ", size=(20, 1)), sg.FileBrowse(key="-IN-")]],
    [sg.Text('İşlem Seçin', size=(20, 1))],
    [sg.Button('Takipçi Listesi', size=(61, 2))],
    [sg.Button('Takip Listesi', size=(61, 2))],
    [sg.Button('Sen onu takip ediyorsun ama o seni etmiyor listesi', size=(61, 2))],
    [sg.Button('Ghost Listesi', size=(61, 2))],
    [sg.Button('Takipten Çık', size=(61, 2))],
    [sg.Button('Takip et', size=(61, 2))],
    [sg.Text('Yazar: Denizsalk', font=('Any 8'))]]

window = sg.Window("Instasalker").Layout(layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    else:
        kullaniciadi = values[0]
        print("kullanıcı adı:              " + kullaniciadi)
        sifre = values[1]
        print("girilen şifre:              " + sifre)
        hedef = values[2]
        dosya = values["-IN-"]
        print("Dosya:                      " + dosya)
        print("hedef kullanıcı adı:        " + hedef)
        print("istenen:                    " + event)
        if event == "Takip Listesi":
            L = instaloader.Instaloader()
            L.login(kullaniciadi, sifre)
            profile = instaloader.Profile.from_username(L.context, hedef)
            follow_list = []
            count = 0
            for followee in profile.get_followers():
                follow_list.append(followee.username)
                file = open(hedef + "takip.txt", "a+")
                file.write(follow_list[count])
                file.write("\n")
                file.close()
                print(follow_list[count])
                count = count + 1
            with open(hedef + "takip.txt") as f:
                c = Counter(c.strip().lower() for c in f if c.strip())
            for line in c:
                if c[line] > 1:
                    print(line)
        if event == "Takipçi Listesi":
            L = instaloader.Instaloader()
            L.login(kullaniciadi, sifre)
            profile = instaloader.Profile.from_username(L.context, hedef)
            follow_list = []
            count = 0
            for followee in profile.get_followees():
                follow_list.append(followee.username)
                file = open(hedef + "takipçiler.txt", "a+")
                file.write(follow_list[count])
                file.write("\n")
                file.close()
                print(follow_list[count])
                count = count + 1
            with open(hedef + "takipçiler.txt") as f:
                c = Counter(c.strip().lower() for c in f if c.strip())  # for case-insensitive search
            for line in c:
                if c[line] > 1:
                    print(line)
        if event == "Sen onu takip ediyorsun ama o seni etmiyor listesi":
            L = instaloader.Instaloader()
            L.login(kullaniciadi, sifre)
            profile = instaloader.Profile.from_username(L.context, hedef)
            followers = set(profile.get_followers())
            followees = set(profile.get_followees())
            badpeoples = followees - followers
            with open("pis-insanlar.txt", 'w') as f:
                for badpeople in badpeoples:
                    print(badpeople.username, file=f)
        if event == "Ghost Listesi":
            L = instaloader.Instaloader()
            L.login(kullaniciadi, sifre)
            profile = instaloader.Profile.from_username(L.context, hedef)
            posts = instaloader.Profile.from_username(L.context, hedef).get_posts()
            likes = set()
            print("Fetching likes of all posts of profile {}.".format(profile.username))
            for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
                print(post)
                likes = likes | set(post.get_likes())
            print("Fetching followers of profile {}.".format(profile.username))
            followers = set(profile.get_followers())
            ghosts = followers - likes
            print("Storing ghosts into file.")
            with open("inactive-users.txt", 'w') as f:
                for ghost in ghosts:
                    print(ghost.username, file=f)
        if event == "Takip et":
            with open(dosya) as f:
                content_list = f.readlines()
            print(content_list)
            content_list = [x.strip() for x in content_list]
            print(content_list)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get("https://www.instagram.com/")
            time.sleep(3)
            driver.find_element("css selector", "input._2hvTZ.pexuQ.zyHYP").click()
            time.sleep(1)
            driver.find_element("css selector", "input._2hvTZ.pexuQ.zyHYP").send_keys(kullaniciadi)
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").click()
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").send_keys(sifre)
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").send_keys(Keys.ENTER)
            time.sleep(4)

            for x in content_list:
                current = "https://www.instagram.com/" + x
                driver.get(current)
                time.sleep(3)
                try:
                    driver.find_element("css selector", "._acas").send_keys(Keys.ENTER)
                except NoSuchElementException:  # spelling error making this code not work as expected
                    pass
                time.sleep(1)
        if event == "Takipten Çık":
            with open(dosya) as f:
                content_list = f.readlines()
            print(content_list)
            content_list = [x.strip() for x in content_list]
            print(content_list)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get("https://www.instagram.com/")
            time.sleep(3)
            driver.find_element("css selector", "input._2hvTZ.pexuQ.zyHYP").click()
            time.sleep(1)
            driver.find_element("css selector", "input._2hvTZ.pexuQ.zyHYP").send_keys(kullaniciadi)
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").click()
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").send_keys(sifre)
            time.sleep(1)
            driver.find_element("css selector", "input[type='password']").send_keys(Keys.ENTER)
            time.sleep(4)
            for x in content_list:
                current = "https://www.instagram.com/" + x
                driver.get(current)
                time.sleep(3)
                try:
                    driver.find_element("css selector", "._acat").send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.find_element("css selector", "button._a9--._a9-_").send_keys(Keys.ENTER)
                    time.sleep(1)
                except NoSuchElementException:  # spelling error making this code not work as expected
                    pass
                time.sleep(1)
window.close()
