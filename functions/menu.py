from sys import version_info
if version_info.major == 2:
    import Tkinter
elif version_info.major == 3:
    import tkinter as tk
    from tkinter import filedialog
from tkinter import *
import re
import json
import requests
import functions.config as config
import fileinput
import threading
import sys
from pynput.keyboard import Key, Controller
#import pygetwindow as gw
import webbrowser
import sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Wnck", "3.0")
from gi.repository import Gtk, Gdk, Wnck




def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def buyitem(whisper):
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
    keyboard.type(whisper)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)




def searchwindowset():
    global parameters
    global name
    item = e.get()


    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": item,
            "stats": [{
                "type": "and",
                "filters": []
            }]
        },
        "sort": {
            "price": "asc"
        }
    }

    name = parameters['query']['name']
    #jprint(parameters)
    response = requests.post("https://www.pathofexile.com/api/trade/search/Metamorph", json=parameters)
    #jprint(response.json())
    query = response.json()["id"]
    result = response.json()["result"][:10]
    #result = re.sub('[!@#$]', '', result)
    result = json.dumps(result)
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('"', '')
    result = result.replace(' ', '')

    #print("https://www.pathofexile.com/api/trade/fetch/{}?query={}".format(result, query))

    response = requests.get("https://www.pathofexile.com/api/trade/fetch/{}?query={}".format(result, query))
    result = response.json()["result"]
    #jprint(result)



    BuyFrame = Tk()
    BuyFrame.configure(background="black")
    BuyFrame.geometry('400x300+200+200')
    BuyFrame.title(name)


    r = 0
    wr = {}
    br = {}
    for d in result:
        if d['listing']['price'] != None:
          amount = d['listing']['price']['amount']
          currency = d['listing']['price']['currency']
          nick = d['listing']['account']['lastCharacterName']
          whisper = d['listing']['whisper']
          if 'corrupted' in d['item']:
              corrupt = d['item']['corrupted']

              wr[r] = tk.Label(BuyFrame, text="price {} {} Corrupt - {}".format(amount, currency, nick), fg="Pink", bg="black").grid(row=r)
              br[r] = tk.Button(BuyFrame, text ="Buy", bg="pink", fg="black", command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

          else:
              wr[r] = tk.Label(BuyFrame, text="price {} {} - {}".format(amount, currency, nick), fg="Pink", bg="black").grid(row=r)
              br[r] = tk.Button(BuyFrame, text ="Buy", bg="pink", fg="black", command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

          r = r + 1
    btn1 = tk.Button(BuyFrame, text = "Show on web", bg="pink", fg="black", command=lambda: webbrowser.open("https://www.pathofexile.com/trade/search/Metamorph/"+ query)).grid(row=r, column=0)
    BuyFrame.call('wm', 'attributes', '.', '-topmost', '1')
    BuyFrame.mainloop()

def setclienttxt():
    clientwindow = tk.Tk()
    clientwindow.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text","*.txt"),("all files","*.*")))
    for line in fileinput.input("functions/config.py", inplace=1):
        if "clienttxt" in line:

            line = line.replace(line,"clienttxt = '{}'".format(clientwindow.filename) )
        sys.stdout.write(line)
    clientwindow.destroy()

    clientwindow.mainloop()

def setsound():
    soundwindow = tk.Tk()
    soundwindow.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Wave","*.wav"),("Mp3","*.mp3"),("all files","*.*")))
    for line in fileinput.input("functions/config.py", inplace=1):
        if "soundfile" in line:

            line = line.replace(line,"soundfile = '{}'".format(soundwindow.filename) )
        sys.stdout.write(line)
    soundwindow.destroy()

    soundwindow.mainloop()

def setty(tytext):
    for line in fileinput.input("functions/config.py", inplace=1):
        if "tytrade" in line:

            line = line.replace(line,"tytrade = '{}'".format(tytext) )
        sys.stdout.write(line)

def createmainmenu():
    global e
    menuwindow = tk.Tk()
    menuwindow.title("Poe Tools")
    menuwindow.configure(background="black")
    menuwindow.geometry('600x300+200+200')
    w = tk.Label(menuwindow, text="Welcome to Poe Tools", fg="Pink", bg="black").grid(row=0, column=2)
    w = tk.Label(menuwindow, text="Unique Item Search", fg="Pink", bg="black").grid(row=1, column=1)
    e = tk.Entry(menuwindow, width=30, fg="Pink", bg="black")
    e.grid(row=1, column=2)

    btn1 = tk.Button(menuwindow, text = "Search", bg="pink", fg="black", command=searchwindowset).grid(row=1, column=3)

    w = tk.Label(menuwindow, text="Client.txt", fg="Pink", bg="black").grid(row=2, column=1)
    f = tk.Entry(menuwindow, width=30, fg="Pink", bg="black")
    f.insert(0, config.clienttxt)
    f.grid(row=2, column=2)
    btn2 = tk.Button(menuwindow, text = "Set", bg="pink", fg="black", command=setclienttxt)
    btn2.grid(row=2, column=3)

    w = tk.Label(menuwindow, text="Trade Sound", fg="Pink", bg="black").grid(row=3, column=1)
    g = tk.Entry(menuwindow, width=30, fg="Pink", bg="black")
    g.insert(0, config.soundfile)
    g.grid(row=3, column=2)
    btn3 = tk.Button(menuwindow, text = "Set", bg="pink", fg="black", command=setsound)
    btn3.grid(row=3, column=3)

    w = tk.Label(menuwindow, text="Ty Text", fg="Pink", bg="black").grid(row=4, column=1)
    g = tk.Entry(menuwindow, width=30, fg="Pink", bg="black")
    g.insert(0, config.tytrade)
    g.grid(row=4, column=2)
    btn3 = tk.Button(menuwindow, text = "Set", bg="pink", fg="black", command=lambda: setty(g.get()))
    btn3.grid(row=4, column=3)

    menuwindow.call('wm', 'attributes', '.', '-topmost', '1')
    menuwindow.mainloop()
