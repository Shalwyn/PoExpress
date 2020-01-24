#!/usr/bin/python
# -*- coding: utf-8 -*-#

from functions.pricecheck import *
from functions.keyfunctions import *
import sys
import functions.config as config
import functions.menu as menu
import functions.tradeget as tradeget
import threading
from tkinter import filedialog
import psutil
import PySimpleGUIQt as sg
import fileinput

menu_def = ['BLANK', 'E&xit']

tray = sg.SystemTray(menu=menu_def, filename=r'icon.png')


import functions.menu as menu
#trayth = threading.Thread(target=icon.run())
#trayth.start()

smtray = threading.Thread(target=menu.createmainmenu)
smtray.start()

keyth = threading.Thread(target=watch_keyboard)
keyth.start()

#trayth = threading.Thread(target=traycreate)
#trayth.start()

prev = ""
prevst = ""
root = Tk()
root.update()
root.withdraw()
DEBUG = False
i = 0

if config.clienttxt == '':
    clientwindow = Tk()
    clientwindow.filename = filedialog.askopenfilename(initialdir="/", title="Please choose your Client.txt",
                                                       filetypes=(("Text", "*.txt"), ("all files", "*.*")))
    for line in fileinput.input("functions/config.py", inplace=1):
        if "clienttxt" in line:
            line = line.replace(line, "clienttxt = '{}'\n".format(clientwindow.filename))
        sys.stdout.write(line)
    clientwindow.destroy()

    clientwindow.mainloop()

originalTime = os.path.getmtime(config.clienttxt)

while True:
    menu_item = tray.Read()
    if menu_item == 'Exit':
        if sys.platform == "linux":
            PROCNAME = "python"
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
        else:
            PROCNAME = "python.exe"

            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()


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

    if os.path.getmtime(config.clienttxt) > originalTime:
        ding = open(config.clienttxt, 'r', encoding='UTF8')
        last_line = ding.readlines()[-1]
        ding.close()
        if tradeget.league in last_line and "@From" in last_line:
            try:
                tradeget.addtabtrade(tradeget.window, tradeget.tasktabs)
            except:
                t18 = threading.Thread(target=tradeget.tradewindow)
                t18.start()
        if tradeget.league in last_line and "@To" in last_line:
            t18 = threading.Thread(target=tradeget.outgoinwindow)
            t18.start()
        if "Redeemer" in last_line and config.redeemer < 3:
            config.redeemer = config.redeemer + 1
            for line in fileinput.input("functions/config.py", inplace=1):
                if "redeemer" in line:
                    line = line.replace(line, "redeemer = {}\n".format(config.redeemer))
                sys.stdout.write(line)
            menu.act1.config(text=config.redeemer)
        if "Crusader" in last_line and config.crusader < 3:
            config.crusader = config.crusader + 1
            for line in fileinput.input("functions/config.py", inplace=1):
                if "crusader" in line:
                    line = line.replace(line, "crusader = {}\n".format(config.crusader))
                sys.stdout.write(line)
            menu.act2.config(text=config.crusader)
        if "Warlord" in last_line and config.warlord < 3:
            config.warlord = config.warlord + 1
            for line in fileinput.input("functions/config.py", inplace=1):
                if "warlord" in line:
                    line = line.replace(line, "warlord = {}\n".format(config.warlord))
                sys.stdout.write(line)
            menu.act3.config(text=config.warlord)
        if "Hunter" in last_line and config.hunter < 3:
            config.hunter = config.hunter + 1
            for line in fileinput.input("functions/config.py", inplace=1):
                if "hunter" in line:
                    line = line.replace(line, "hunter = {}\n".format(config.hunter))
                sys.stdout.write(line)
            menu.act4.config(text=config.hunter)
            # menu.act1.configure(text=config.redeemer)

        originalTime = os.path.getmtime(config.clienttxt)
