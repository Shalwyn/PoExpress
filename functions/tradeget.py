#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from sys import version_info
if version_info.major == 2:
    import Tkinter
elif version_info.major == 3:
    import tkinter as tk
from playsound import playsound
import re
import threading
from pynput.keyboard import Key, Controller

from datetime import datetime
import sys
from tkinter import ttk
if sys.platform == "linux":
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("Wnck", "3.0")
    from gi.repository import Gtk, Gdk, Wnck
else:
    import pygetwindow as gw
import sys
import configparser
import os
import subprocess

config = configparser.ConfigParser()
if sys.platform == "linux":
    config.read('{}/config.ini'.format(os.getcwd()))
else:
    config.read('{}\config.ini'.format(os.getcwd()))

league = "Metamorph"

def hideout(seller):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)
    keyboard.press(Key.shift_l)
    time.sleep(0.1)
    keyboard.press('7')
    time.sleep(0.1)
    keyboard.release('7')
    time.sleep(0.1)
    keyboard.release(Key.shift_l)
    (0.1)
    keyboard.type("hideout {}".format(seller[:-1]))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def sendinvite(nicktoinvite):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)
    keyboard.press(Key.shift_l)
    time.sleep(0.1)
    keyboard.press('7')
    time.sleep(0.1)
    keyboard.release('7')
    time.sleep(0.1)
    keyboard.release(Key.shift_l)
    (0.1)
    keyboard.type("invite {}".format(nicktoinvite))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def finditem(itemtosearch):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press('f')
    keyboard.release(Key.ctrl)
    keyboard.release('f')

    keyboard.type("{}".format(itemtosearch))



def sendtrade(nicktotrade):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)
    keyboard.press(Key.shift_l)
    time.sleep(0.1)
    keyboard.press('7')
    time.sleep(0.1)
    keyboard.release('7')
    time.sleep(0.1)
    keyboard.release(Key.shift_l)
    (0.1)
    keyboard.type("tradewith {}".format(nicktotrade))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def sendty(nicktotrade):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type(u'\u0040')
    time.sleep(0.1)
    keyboard.type("{} {}".format(nicktotrade, config['FILES']['tytrade']))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def sendbusy(nicktotrade):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type(u'\u0040')
    time.sleep(0.1)
    keyboard.type("{} {}".format(nicktotrade, "Sorry busy right now will invite you when im done"))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    
def sendinter(buyer, item):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type(u'\u0040')
    time.sleep(0.1)
    keyboard.type("{} Hey, still interested in my: {} ?".format(buyer, item))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def sendsold(nicktotrade, item):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type(u'\u0040')
    time.sleep(0.1)
    keyboard.type("{} Sorry my {} is actually sold".format(nicktotrade, item))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def kickparty(nicktokick, window, tasktabs):
    if sys.platform == "linux":
        subprocess.Popen("wmctrl -a Path of Exile", stdout=subprocess.PIPE, shell=True)
    else:
        notepadWindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadWindow.activate()

    time.sleep(1)

    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)
    keyboard.press(Key.shift_l)
    time.sleep(0.1)
    keyboard.press('7')
    time.sleep(0.1)
    keyboard.release('7')
    time.sleep(0.1)
    keyboard.release(Key.shift_l)
    (0.1)
    keyboard.type("kick {}".format(nicktokick))
    time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    tasktabs.forget(tasktabs.select())
    if tasktabs.select() is "":
        window.withdraw()  

def forgettabs(tasktabs):
    tasktabs.forget(tasktabs.select())
    if tasktabs.select() is "":
        window.withdraw()  
    


def addtabtrade(window, tasktabs, line):

    dateTimeObj = datetime.now()
    now = dateTimeObj.strftime("%H:%M:%S")
    sound = config['FILES']['soundfile']


    last_line = line

    splitmsg = last_line.split()
    if 'wtb' in splitmsg and "@From" in splitmsg and "(stash" in splitmsg:
        buyer = splitmsg[splitmsg.index("wtb") - 1]
        del splitmsg[0:splitmsg.index("wtb")]
        item = splitmsg[splitmsg.index("wtb") + 1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for") + 1:splitmsg.index("for") + 3]
        stash = splitmsg[splitmsg.index(league) + 1:splitmsg.index(league) + 11]
        buyer = buyer[:-1]
        playsound("{}".format(sound))
    if 'Hi,' in splitmsg and "@From" in splitmsg and "(stash" in splitmsg:
        buyer = splitmsg[splitmsg.index("Hi,") - 1]
        del splitmsg[0:splitmsg.index("Hi,")]
        buyer = buyer[:-1]
        item = splitmsg[splitmsg.index("your") + 1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for") + 1:splitmsg.index("for") + 3]
        stash = splitmsg[splitmsg.index(league) + 1:splitmsg.index(league) + 11]
        playsound("{}".format(sound))
    if "for" in splitmsg and "my" in splitmsg:
        buyer = splitmsg[1]
        buyer = buyer[:-1]
        item = splitmsg[splitmsg.index("your") + 1:splitmsg.index("for")]
        price = splitmsg[splitmsg.index("my") + + 1:splitmsg.index("in")]
        stash = ""
        playsound("{}".format(sound))

    windowtext = " ".join(item)
    windowprice = " ".join(price)
    windowstash = " ".join(stash)

    window.update()
    window.deiconify()

    Tab = ttk.Frame(tasktabs)
        
    tasktabs.add(Tab, text=buyer)
    tasktabs.grid(row=0, column=0, sticky="W")
    T = tk.Text(Tab, height=10, width=60, fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    T.grid(row=1, column=0, columnspan=6, sticky="nsew")
    T.insert(tk.END, "Item: {} \n".format(windowtext))
    T.insert(tk.END, "Price: {} \n".format(windowprice))
    T.insert(tk.END, "{} \n".format(windowstash))
    T.insert(tk.END, "{} \n".format(now))
    tk.Button(Tab, text="Invite", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: sendinvite(buyer)).grid(row=2, column=0)
    tk.Button(Tab, text="Sold", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: sendsold(buyer, item)).grid(row=2, column=1)
    tk.Button(Tab, text="Busy", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: sendbusy(buyer)).grid(
        row=2, column=2)
    tk.Button(Tab, text="Interested?", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: sendinter(buyer, windowtext)).grid(
        row=2, column=3)
    tk.Button(Tab, text="Find Item", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: finditem(windowtext)).grid(row=3, column=0)
    tk.Button(Tab, text="Trade", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: sendtrade(buyer)).grid(
        row=3, column=1)
    tk.Button(Tab, text="Ty", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: sendty(buyer)).grid(row=3,
                                                                                                                  column=2)
    tk.Button(Tab, text="Kick", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: kickparty(buyer, window, tasktabs)).grid(row=3, column=3)
    tk.Button(Tab, text="Close", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: forgettabs(tasktabs)).grid(row=4, column=2)
    

def tradewindowthreat(lastline):
     ttw = threading.Thread(target=tradewindow, kwargs={'line': lastline})
     ttw.start()



def tradewindow(line=""):
   
    global window
    
    
    global tasktabs
    window = tk.Tk()
        
    window.title("Trade")
    
    style = ttk.Style(window)
    
    style.theme_use("clam")
    style.configure("TNotebook", background=config['colors']['bgcolor'])
    style.configure("TNotebook.Tab", background=config['colors']['bgcolor'], foreground=config['colors']['fgcolor'])
    style.configure("TFrame", background=config['colors']['bgcolor'])
    
    tasktabs = ttk.Notebook(window)
  
    def on_close():
        tasktabs.forget(tasktabs.select())
     
        window.withdraw()
  
    window.call('wm', 'attributes', '.', '-topmost', '1')
    addtabtrade(window, tasktabs, line)
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
  

def outgoinwindow():
    clientding = open(config['FILES']['clienttxt'], 'r', encoding='UTF8')
    last_line = clientding.readlines()[-1]
    clientding.close()
    splitmsg = last_line.split()
    if 'wtb' in splitmsg and "@To" in splitmsg and "(stash" in splitmsg:
        seller = splitmsg[splitmsg.index("wtb")-1]
        del splitmsg[0:splitmsg.index("wtb")]
        item = splitmsg[splitmsg.index("wtb")+1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for")+1:splitmsg.index("for")+3]


    if 'Hi,' in splitmsg  and "@To" in splitmsg and "(stash" in splitmsg:
        seller = splitmsg[splitmsg.index("@To")+1]
        del splitmsg[0:splitmsg.index("Hi,")]

        item = splitmsg[splitmsg.index("your")+1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for")+1:splitmsg.index("for")+3]
    if "for" in splitmsg and "my" in splitmsg:
        seller = splitmsg[1]
        seller = seller[:-1]
        item = splitmsg[splitmsg.index("your") + 1:splitmsg.index("for")]
        price = splitmsg[splitmsg.index("my") + + 1:splitmsg.index("in")]
 
 


    dateTimeObj = datetime.now()
    now = dateTimeObj.strftime("%H:%M:%S")
    window = tk.Tk()
    window.title("Trade")
    window.configure(background=config['colors']['fgcolor'])
    windowtext = " ".join(item)
    windowprice = " ".join(price)
    T = tk.Text(window, height=10, width=60, fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    T.grid(row=0, column=0, columnspan=3,  sticky="nsew")
    T.insert(tk.END, "Nick: {} \n".format(seller))
    T.insert(tk.END, "Item: {} \n".format(windowtext))
    T.insert(tk.END, "Price: {} \n".format(windowprice))
    T.insert(tk.END, "{} \n".format(now))
    tk.Button(window, text = "Visit Hideout", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: hideout(seller)).grid(row=1, column=0)
    tk.Button(window, text = "Ty", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: sendty(seller)).grid(row=1, column=1)

    window.call('wm', 'attributes', '.', '-topmost', '1')
#    window.after(0, readclient())
    window.mainloop()
