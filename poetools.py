#!/usr/bin/python
# -*- coding: utf-8 -*-#

from functions.pricecheck import *
from functions.keyfunctions import *
import sys
import functions.config as config
import functions.tradeget as tradeget
import threading
import time

from tkinter import filedialog
import psutil
import PySimpleGUIQt as sg
import configparser
import functions.menu as menu

menu_def = ['BLANK', 'E&xit']

smtray = threading.Thread(target=menu.createmainmenu)
smtray.start()

keyth = threading.Thread(target=watch_keyboard)
keyth.start()

prev = ""
prevst = ""
root = Tk()
root.update()
root.withdraw()
DEBUG = False
i = 0
global lastlinesold
global lastlinesnew

config = configparser.ConfigParser()
if sys.platform == "linux":
    config.read('{}/config.ini'.format(os.getcwd()))
else:
    config.read('{}\config.ini'.format(os.getcwd()))



def checkclienttxt():
    try:
        open(config['FILES']['clienttxt'] , "r")
    except IOError:
        clientwindow = Tk()
        clientwindow.filename = filedialog.askopenfilename(initialdir="/", title="Please choose your Client.txt",
                                                           filetypes=(("Text", "*.txt"), ("all files", "*.*")))
        config['FILES']['clienttxt'] = clientwindow.filename
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        clientwindow.destroy()

        clientwindow.mainloop()


checkclienttxt()

originalTime = os.path.getmtime(config['FILES']['clienttxt'])

def traymake():
    tray = sg.SystemTray(menu=menu_def, filename=r'icon.png')
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
                PROCNAME = "poetools.exe"

                for proc in psutil.process_iter():
                    # check whether the process name matches
                    if proc.name() == PROCNAME:
                        proc.kill()

trayth = threading.Thread(target=traymake)
trayth.start()

lastlinesold = sum(1 for line in open(config['FILES']['clienttxt'], 'r', encoding='UTF8'))
lastseenline = ""

while True:

    try:
        data = root.clipboard_get()
    except (TclError, UnicodeDecodeError):  # ignore non-text clipboard contents
        continue

    splitdata = data.splitlines()
    if "Rarity: Unique" in data and config['FILES'].getint('statsearch') == 0:
        if data != prev:
            prev = data
            buildunique(data)
            t80 = threading.Thread(target=buildpricewindow)
            t80.start()

    elif "Rarity: Unique" in data and config['FILES'].getint('statsearch') == 1:

        if data != prevst:
            prevst = data
            prev = data
            builduniquestat(data)
            t81 = threading.Thread(target=buildpricewindow)
            t81.start()
            config = configparser.ConfigParser()
            if sys.platform == "linux":
                config.read('{}/config.ini'.format(os.getcwd()))
            else:
                config.read('{}\config.ini'.format(os.getcwd()))
            config['FILES']['statsearch'] = str(0)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)


    elif "Map Tier:" in data and ("Rarity: Rare" in data or "Rarity: Normal" in data or "Rarity: Magic" in data):
        if data != prev:
            prev = data
            buildmap(data)
            t82 = threading.Thread(target=buildpricewindow)
            t82.start()

    elif "Rarity: Currency" in data or "Rarity: Divination Card" in data:
        if data != prev:
            prev = data
            buildcurrency(data)
            t83 = threading.Thread(target=buildpricewindow)
            t83.start()

    elif "Rarity: Gem" in data:

        if data != prev:
            prev = data
            buildgem(data)
            t84 = threading.Thread(target=buildpricewindow)
            t84.start()

    elif "Rarity: Rare" in data and splitdata[3] == "--------":
        if data != prev:
            prev = data
            buildrareitem(data)
            t85 = threading.Thread(target=buildpricewindow)
            t85.start()

    elif "Rarity: Normal" in data:
        if data != prev:
            prev = data
            buildnormal(data)
            t84 = threading.Thread(target=buildpricewindow)
            t84.start()

    time.sleep(0.5)
    print(os.path.getmtime(config['FILES']['clienttxt']), originalTime)
    if os.path.getmtime(config['FILES']['clienttxt']) > originalTime:
        config = configparser.ConfigParser()
        if sys.platform == "linux":
            config.read('{}/config.ini'.format(os.getcwd()))
        else:
            config.read('{}\config.ini'.format(os.getcwd()))
        ding = open(config['FILES']['clienttxt'], 'r', encoding='UTF8')
        lastlinesnew = sum(1 for line in ding)
        
        while lastlinesold < lastlinesnew:
            last_line = open(config['FILES']['clienttxt'], 'r', encoding='UTF8').readlines()[lastlinesold]

            if tradeget.league in last_line and "@From" in last_line:
                try:
                    tradeget.addtabtrade(tradeget.window, tradeget.tasktabs, lastlinesold, lastlinesnew)
                except:
                    t18 = threading.Thread(target=tradeget.tradewindow, kwargs={'lastlinesold': lastlinesold, 'lastlinesnew': lastlinesnew})
                    t18.start()


            if tradeget.league in last_line and "@To" in last_line:
                t18 = threading.Thread(target=tradeget.outgoinwindow)
                t18.start()

            if "Redeemer" in last_line and config['awakener'].getint('redeemer') < 3 and "Redeember" not in lastseenline:
                newwrite = config['awakener'].getint('redeemer') + 1
                config.set('awakener', 'redeemer', str(newwrite))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                menu.act1.config(text=config['awakener'].getint('redeemer'))


            if "Crusader" in last_line and config['awakener'].getint('crusader') < 3 and "Crusader" not in lastseenline:
                newwrite = config['awakener'].getint('crusader') + 1
                config.set('awakener', 'crusader', str(newwrite))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                menu.act2.config(text=config['awakener'].getint('crusader'))

            if "Warlord" in last_line and config['awakener'].getint('warlord') < 3 and "Warlord" not in lastseenline:
                newwrite = config['awakener'].getint('warlord') + 1
                config.set('awakener', 'warlord', str(newwrite))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                menu.act3.config(text=config['awakener'].getint('warlord'))

            if "Hunter" in last_line and config['awakener'].getint('hunter') < 3 and "Hunter" not in lastseenline:
                newwrite = config['awakener'].getint('hunter') + 1
                config.set('awakener', 'hunter', str(newwrite))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                menu.act4.config(text=config['awakener'].getint('hunter'))
                # menu.act1.configure(text=config.redeemer)
            lastlinesold = lastlinesold + 1
            time.sleep(1)
            lastseenline = last_line
        ding.close()
        originalTime = os.path.getmtime(config['FILES']['clienttxt'])
