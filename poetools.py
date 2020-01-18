#!/usr/bin/python
# -*- coding: utf-8 -*-#

import os, time
from tkinter import *
from playsound import playsound
from functions.tradeget import *
from functions.pricecheck import *
from functions.keyfunctions import *
import functions.config as config
import threading
from look import *

ttray = threading.Thread(target=traycreate)
ttray.start()

#threadmain1 = threading.Thread(target=startread())
#threadmain1.start()

#threadmain2 = threading.Thread(target=startcheckclip())
#threadmain2.start()

prev = ""
prevst = ""
root = Tk()
#root.wm_attributes("-topmost", 1)
root.update()
root.withdraw()
DEBUG = False
i = 0
watch_keyboard()

try:
    f = open("C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt")
    fileName = 'C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt'
except IOError:
    print("")



try:
    f = open("C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt")
    fileName = 'C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt'
except IOError:
    print("")

originalTime = os.path.getmtime(fileName)
while True:
    try:
        data = root.clipboard_get()
    except (TclError, UnicodeDecodeError):  # ignore non-text clipboard contents
        continue

    splitdata = data.splitlines()
    if "Rarity: Unique" in data and config.statsearch == 0:
        if data != prev:

            prev = data
            buildunique(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()

    elif "Rarity: Unique" in data and config.statsearch == 1:
        if data != prevst:
            prevst = data
            prev = data
            builduniquestat(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()
            config.statsearch = 0

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



    elif "Rarity: Rare" in data and splitdata[3] == "--------":
        if data != prev:
            prev = data
            buildrareitem(data)
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
