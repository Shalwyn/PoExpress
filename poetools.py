#!/usr/bin/python
# -*- coding: utf-8 -*-#

import os, time
from tkinter import *
from playsound import playsound
from functions.tradeget import *
from functions.pricecheck import *
from functions.keyfunctions import *
import functions.config as config
from functions.menu import *
import threading
#from look import *

#ttray = threading.Thread(target=traycreate)
#ttray.start()

smtray = threading.Thread(target=createmainmenu)
smtray.start()

keyth = threading.Thread(target=watch_keyboard)
keyth.start()



prev = ""
prevst = ""
root = Tk()
#root.wm_attributes("-topmost", 1)
root.update()
root.withdraw()
DEBUG = False
i = 0
#watch_keyboard()


originalTime = os.path.getmtime(config.clienttxt)
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
            print("statsearch = 0")

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

    if(os.path.getmtime(config.clienttxt) > originalTime):
        ding = open(config.clienttxt, 'r', encoding='UTF8')
        last_line = ding.readlines()[-1]
        ding.close()
        if league in last_line and "@From" in last_line:
            t18 = threading.Thread(target=tradewindow)
            t18.start()
        if league in last_line and "@To" in last_line:
            t18 = threading.Thread(target=outgoinwindow)
            t18.start()
        originalTime = os.path.getmtime(config.clienttxt)
