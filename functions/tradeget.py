#!/usr/bin/python
# -*- coding: utf-8 -*-#

from sys import version_info
if version_info.major == 2:
    import Tkinter
elif version_info.major == 3:
    import tkinter as tk
import os, time
from playsound import playsound
import re
from pynput.keyboard import Key, Controller
import functions.config as config
import threading
from datetime import datetime
import keyboard
import sys
if sys.platform == "linux":
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("Wnck", "3.0")
    from gi.repository import Gtk, Gdk, Wnck
else:
    import pygetwindow as gw

league = "Metamorph"

def hideout(seller):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()



    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type("/hideout {}".format(seller[:-1]))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def sendinvite(nicktoinvite):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type("/invite {}".format(nicktoinvite))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def finditem(itemtosearch):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()


    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press('f')
    keyboard.release(Key.ctrl)
    keyboard.release('f')

    keyboard.type("{}".format(itemtosearch))



def sendtrade(nicktotrade):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()


    keyboard = Controller()
    keyboard.type("\n/tradewith {}\n".format(nicktotrade))

def sendty(nicktotrade):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()



    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type("@{} {}".format(nicktotrade, config.tytrade))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)



def kickparty(nicktokick, window):
    if sys.platform == "linux":
        titlePattern = re.compile("Path of Exile")

        Gtk.init([])  # necessary if not using a Gtk.main() loop
        screen = Wnck.Screen.get_default()
        screen.force_update()  # recommended per Wnck documentation

        window_list = screen.get_windows()
        for w in window_list:
            if titlePattern.match(w.get_name()):
                w.activate(0)
    else:
        regex = "Path of Exile"
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()



    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type("/kick {}".format(nicktokick))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    window.destroy()

def tradewindow():
    #global window
    sound = config.soundfile

    clientding = open(config.clienttxt, 'r', encoding='UTF8')
    last_line = clientding.readlines()[-1]
    clientding.close()
    splitmsg = last_line.split()
    if 'wtb' in splitmsg and "@From" in splitmsg:
        buyer = splitmsg[splitmsg.index("wtb")-1]
        del splitmsg[0:splitmsg.index("wtb")]
        buyer = buyer[:-1]
        playsound(sound)
    if 'Hi,' in splitmsg  and "@From" in splitmsg:
        buyer = splitmsg[splitmsg.index("Hi,")-1]
        del splitmsg[0:splitmsg.index("Hi,")]
        buyer = buyer[:-1]
        item = splitmsg[splitmsg.index("your")+1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for")+1:splitmsg.index("for")+3]
        stash = splitmsg[splitmsg.index(league)+1:splitmsg.index(league)+11]
        playsound(sound)

    dateTimeObj = datetime.now()
    now = dateTimeObj.strftime("%H:%M:%S")
    window = tk.Tk()
    window.title("Trade")
    window.configure(background=config.fgcolor)
    windowtext = " ".join(item)
    windowprice = " ".join(price)
    windowstash = " ".join(stash)
    T = tk.Text(window, height=10, width=60, fg=config.textcolor, bg=config.bgcolor)
    T.grid(row=0, column=0, columnspan=5,  sticky="nsew")
    T.insert(tk.END, "Nick: {} \n".format(buyer))
    T.insert(tk.END, "Item: {} \n".format(windowtext))
    T.insert(tk.END, "Price: {} \n".format(windowprice))
    T.insert(tk.END, "{} \n".format(windowstash))
    T.insert(tk.END, "{} \n".format(now))
    btn1 = tk.Button(window, text = "Invite", bg=config.bgcolor, fg=config.fgcolor, command=lambda: sendinvite(buyer)).grid(row=1, column=0)
    btn2 = tk.Button(window, text = "Trade", bg=config.bgcolor, fg=config.fgcolor, command=lambda: sendtrade(buyer)).grid(row=1, column=1)
    btn5 = tk.Button(window, text = "Find Item", bg=config.bgcolor, fg=config.fgcolor, command=lambda: finditem(windowtext)).grid(row=1, column=2)
    btn4 = tk.Button(window, text = "Ty", bg=config.bgcolor, fg=config.fgcolor, command=lambda: sendty(buyer)).grid(row=1, column=3)
    btn3 = tk.Button(window, text = "Kick", bg=config.bgcolor, fg=config.fgcolor, command=lambda: kickparty(buyer, window)).grid(row=1, column=4)

    window.call('wm', 'attributes', '.', '-topmost', '1')
#    window.after(0, readclient())
    window.mainloop()


def outgoinwindow():
    clientding = open(config.clienttxt, 'r', encoding='UTF8')
    last_line = clientding.readlines()[-1]
    clientding.close()
    splitmsg = last_line.split()
    if 'wtb' in splitmsg and "@To" in splitmsg:
        buyer = splitmsg[splitmsg.index("wtb")-1]
        del splitmsg[0:splitmsg.index("wtb")]
        buyer = buyer[:-1]

    if 'Hi,' in splitmsg  and "@To" in splitmsg:
        print("here")
        seller = splitmsg[splitmsg.index("@To")+1]
        del splitmsg[0:splitmsg.index("Hi,")]

        item = splitmsg[splitmsg.index("your")+1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for")+1:splitmsg.index("for")+3]
        stash = splitmsg[splitmsg.index(league)+1:splitmsg.index(league)+11]


    dateTimeObj = datetime.now()
    now = dateTimeObj.strftime("%H:%M:%S")
    window = tk.Tk()
    window.title("Trade")
    window.configure(background=config.fgcolor)
    windowtext = " ".join(item)
    windowprice = " ".join(price)
    windowstash = " ".join(stash)
    T = tk.Text(window, height=10, width=60, fg=config.textcolor, bg=config.bgcolor)
    T.grid(row=0, column=0, columnspan=3,  sticky="nsew")
    T.insert(tk.END, "Nick: {} \n".format(seller))
    T.insert(tk.END, "Item: {} \n".format(windowtext))
    T.insert(tk.END, "Price: {} \n".format(windowprice))
    T.insert(tk.END, "{} \n".format(now))
    btn1 = tk.Button(window, text = "Visit Hideout", bg=config.bgcolor, fg=config.fgcolor, command=lambda: hideout(seller)).grid(row=1, column=0)
    btn2 = tk.Button(window, text = "Ty", bg=config.bgcolor, fg=config.fgcolor, command=lambda: sendty(seller)).grid(row=1, column=1)

    window.call('wm', 'attributes', '.', '-topmost', '1')
#    window.after(0, readclient())
    window.mainloop()
