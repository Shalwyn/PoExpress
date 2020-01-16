import os, time
from tkinter import *
from playsound import playsound
from functions.tradeget import *
from functions.pricecheck import *
from functions.keyfunctions import *
import threading

#threadmain1 = threading.Thread(target=startread())
#threadmain1.start()

#threadmain2 = threading.Thread(target=startcheckclip())
#threadmain2.start()

prev = ""
root = Tk()
#root.wm_attributes("-topmost", 1)
root.update()
root.withdraw()
DEBUG = False
i = 0
watch_keyboard()
fileName = 'C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt'
originalTime = os.path.getmtime(fileName)
while True:
    try:
        data = root.clipboard_get()
    except (TclError, UnicodeDecodeError):  # ignore non-text clipboard contents
        continue


    if "Rarity: Unique" in data:
        if data != prev:
            prev = data
            buildunique(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()

    elif "Map Tier:" in data and "Rarity: Rare" in data or "Rarity: Normal" in data or "Rarity: Magic" in data:
        if data != prev:
            prev = data
            buildmap(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()

    elif "Rarity: Currency" in data or "Rarity: Divination Card" in data:
        if data != prev:
            prev = data
            buildcurrency(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()

    elif "Rarity: Gem" in data:
        if data != prev:
            prev = data
            buildgem(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()

    time.sleep(0.5)

    if(os.path.getmtime(fileName) > originalTime):
        ding = open('C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt', 'r', encoding='UTF8')
        last_line = ding.readlines()[-1]
        ding.close()
        if league in last_line:
            t1 = threading.Thread(target=tradewindow)
            t1.start()
        originalTime = os.path.getmtime(fileName)
