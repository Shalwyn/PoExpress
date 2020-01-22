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

import webbrowser
import sys

if sys.platform == "linux":
    import gi

    gi.require_version("Gtk", "3.0")
    gi.require_version("Wnck", "3.0")
    from gi.repository import Gtk, Gdk, Wnck
else:
    import pygetwindow as gw
from tkinter.colorchooser import askcolor


global e


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
        notepadwindow = gw.getWindowsWithTitle('Path of Exile')[0]
        notepadwindow.activate()

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
    response = requests.post("https://www.pathofexile.com/api/trade/search/Metamorph", json=parameters)
    query = response.json()["id"]
    result = response.json()["result"][:10]
    result = json.dumps(result)
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('"', '')
    result = result.replace(' ', '')

    response = requests.get("https://www.pathofexile.com/api/trade/fetch/{}?query={}".format(result, query))
    result = response.json()["result"]

    buy_frame = Tk()
    buy_frame.configure(background=config.bgcolor)
    buy_frame.geometry('400x300+200+200')
    buy_frame.title(name)

    r = 0
    wr = {}
    br = {}
    for d in result:
        if d['listing']['price'] is not None:
            amount = d['listing']['price']['amount']
            currency = d['listing']['price']['currency']
            nick = d['listing']['account']['lastCharacterName']
            whisper = d['listing']['whisper']
            if 'corrupted' in d['item']:
                corrupt = d['item']['corrupted']

                wr[r] = tk.Label(buy_frame, text="price {} {} Corrupt - {}".format(amount, currency, nick),
                                 fg=config.textcolor, bg=config.bgcolor).grid(row=r)
                br[r] = tk.Button(buy_frame, text="Buy", bg=config.bgcolor, fg=config.fgcolor,
                                  command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

            else:
                wr[r] = tk.Label(buy_frame, text="price {} {} - {}".format(amount, currency, nick), fg=config.textcolor,
                                 bg=config.bgcolor).grid(row=r)
                br[r] = tk.Button(buy_frame, text="Buy", bg=config.bgcolor, fg=config.fgcolor,
                                  command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

            r = r + 1
    btn1 = tk.Button(buy_frame, text="Show on web", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: webbrowser.open(
                         "https://www.pathofexile.com/trade/search/Metamorph/" + query)).grid(row=r, column=0)
    buy_frame.call('wm', 'attributes', '.', '-topmost', '1')
    buy_frame.mainloop()


def setclienttxt():
    clientwindow = tk.Tk()
    clientwindow.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                       filetypes=(("Text", "*.txt"), ("all files", "*.*")))
    for line in fileinput.input("functions/config.py", inplace=1):
        if "clienttxt" in line:
            line = line.replace(line, "clienttxt = '{}'".format(clientwindow.filename))
        sys.stdout.write(line)
    clientwindow.destroy()

    clientwindow.mainloop()


def setsound():
    soundwindow = tk.Tk()
    soundwindow.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
        ("Wave", "*.wav"), ("Mp3", "*.mp3"), ("all files", "*.*")))
    for line in fileinput.input("functions/config.py", inplace=1):
        if "soundfile" in line:
            line = line.replace(line, "soundfile = '{}'".format(soundwindow.filename))
        sys.stdout.write(line)
    soundwindow.destroy()

    soundwindow.mainloop()


def setty(tytext):
    for line in fileinput.input("functions/config.py", inplace=1):
        if "tytrade" in line:
            line = line.replace(line, "tytrade = '{}'".format(tytext))
        sys.stdout.write(line)


def startopt():
    optray = threading.Thread(target=creatoptions)
    optray.start()


def stcolor(which, entry):
    (triple, hexstr) = askcolor()
    if which == "fgcolor":
        for line in fileinput.input("functions/config.py", inplace=1):
            if "fgcolor" in line:
                line = line.replace(line, "fgcolor = '{}'\n".format(hexstr))
            sys.stdout.write(line)

    elif which == "bgcolor":
        for line in fileinput.input("functions/config.py", inplace=1):
            if "bgcolor" in line:
                line = line.replace(line, "bgcolor = '{}'\n".format(hexstr))
            sys.stdout.write(line)

    elif which == "textcolor":
        for line in fileinput.input("functions/config.py", inplace=1):
            if "textcolor" in line:
                line = line.replace(line, "textcolor = '{}'\n".format(hexstr))
            sys.stdout.write(line)

    entry.delete(0, 100)
    entry.insert(0, hexstr)


def resetcount(awakener):
    if awakener == "redeemer":
        config.redeemer = 0
        for line in fileinput.input("functions/config.py", inplace=1):
            if "redeemer" in line:
                line = line.replace(line, "redeemer = {}\n".format(config.redeemer))
            sys.stdout.write(line)
        act1.config(text=config.redeemer)
    if awakener == "crusader":
        config.crusader = 0
        for line in fileinput.input("functions/config.py", inplace=1):
            if "crusader" in line:
                line = line.replace(line, "crusader = {}\n".format(config.crusader))
            sys.stdout.write(line)
        act2.config(text=config.crusader)
    if awakener == "warlord":
        config.warlord = 0
        for line in fileinput.input("functions/config.py", inplace=1):
            if "warlord" in line:
                line = line.replace(line, "warlord = {}\n".format(config.warlord))
            sys.stdout.write(line)
        act3.config(text=config.warlord)
    if awakener == "hunter":
        config.hunter = 0
        for line in fileinput.input("functions/config.py", inplace=1):
            if "hunter" in line:
                line = line.replace(line, "hunter = {}\n".format(config.hunter))
            sys.stdout.write(line)
        act4.config(text=config.hunter)


def createmainmenu():
    global act1
    global act2
    global act3
    global act4

    menuwindow = tk.Tk()
    menuwindow.title("Poe Tools")
    menuwindow.configure(background=config.bgcolor)
    menuwindow.geometry('350x200+200+200')
    w = tk.Label(menuwindow, text="Welcome to Poe Tools", fg=config.textcolor, bg=config.bgcolor).grid(row=0, column=2)
    w = tk.Label(menuwindow, text="Unique Item Search", fg=config.textcolor, bg=config.bgcolor).grid(row=1, column=1)
    e = tk.Entry(menuwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    e.grid(row=1, column=2)
    btn1 = tk.Button(menuwindow, text="Search", bg=config.bgcolor, fg=config.fgcolor, command=searchwindowset).grid(
        row=1, column=3)

    at1 = tk.Label(menuwindow, text="Redeemer: ", fg=config.textcolor, bg=config.bgcolor).grid(row=2, column=1)
    act1 = tk.Label(menuwindow, text=config.redeemer, fg=config.textcolor, bg=config.bgcolor)
    act1.grid(row=2, column=2)
    bta1 = tk.Button(menuwindow, text="reset", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: resetcount("redeemer")).grid(row=2, column=3)

    at2 = tk.Label(menuwindow, text="Crusader: ", fg=config.textcolor, bg=config.bgcolor).grid(row=3, column=1)
    act2 = tk.Label(menuwindow, text=config.crusader, fg=config.textcolor, bg=config.bgcolor)
    act2.grid(row=3, column=2)
    bta2 = tk.Button(menuwindow, text="reset", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: resetcount("crusader")).grid(row=3, column=3)

    at3 = tk.Label(menuwindow, text="Warlord: ", fg=config.textcolor, bg=config.bgcolor).grid(row=4, column=1)
    act3 = tk.Label(menuwindow, text=config.warlord, fg=config.textcolor, bg=config.bgcolor)
    act3.grid(row=4, column=2)
    bta3 = tk.Button(menuwindow, text="reset", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: resetcount("warlord")).grid(row=4, column=3)

    at4 = tk.Label(menuwindow, text="Hunter: ", fg=config.textcolor, bg=config.bgcolor).grid(row=5, column=1)
    act4 = tk.Label(menuwindow, text=config.hunter, fg=config.textcolor, bg=config.bgcolor)
    act4.grid(row=5, column=2)
    bta4 = tk.Button(menuwindow, text="reset", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: resetcount("hunter")).grid(row=5, column=3)

    btnop = tk.Button(menuwindow, text="Options", bg=config.bgcolor, fg=config.fgcolor, command=startopt).grid(row=6,
                                                                                                               column=1)

    menuwindow.call('wm', 'attributes', '.', '-topmost', '1')
    menuwindow.mainloop()


def creatoptions():
    optionwindow = tk.Tk()
    optionwindow.title("Options")
    optionwindow.configure(background=config.bgcolor)
    optionwindow.geometry('600x300+200+200')
    w = tk.Label(optionwindow, text="Client.txt", fg=config.textcolor, bg=config.bgcolor).grid(row=2, column=1)
    f = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    f.insert(0, config.clienttxt)
    f.grid(row=2, column=2)
    btn2 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor, command=setclienttxt)
    btn2.grid(row=2, column=3)

    w = tk.Label(optionwindow, text="Trade Sound", fg=config.textcolor, bg=config.bgcolor).grid(row=3, column=1)
    g = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    g.insert(0, config.soundfile)
    g.grid(row=3, column=2)
    btn3 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor, command=setsound)
    btn3.grid(row=3, column=3)

    w = tk.Label(optionwindow, text="Ty Text", fg=config.textcolor, bg=config.bgcolor).grid(row=4, column=1)
    g = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    g.insert(0, config.tytrade)
    g.grid(row=4, column=2)
    btn4 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor, command=lambda: setty(g.get()))
    btn4.grid(row=4, column=3)

    w = tk.Label(optionwindow, text="Button Foreground Color", fg=config.textcolor, bg=config.bgcolor).grid(row=5,
                                                                                                            column=1)
    g4 = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    g4.insert(0, config.fgcolor)
    g4.grid(row=5, column=2)
    btn5 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: stcolor("fgcolor", g4))
    btn5.grid(row=5, column=3)

    w = tk.Label(optionwindow, text="Button Background Color", fg=config.textcolor, bg=config.bgcolor).grid(row=6,
                                                                                                            column=1)
    g5 = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    g5.insert(0, config.bgcolor)
    g5.grid(row=6, column=2)
    btn5 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: stcolor("bgcolor", g5))
    btn5.grid(row=6, column=3)

    w = tk.Label(optionwindow, text="Text Color", fg=config.textcolor, bg=config.bgcolor).grid(row=7, column=1)
    g6 = tk.Entry(optionwindow, width=30, fg=config.fgcolor, bg=config.bgcolor)
    g6.insert(0, config.textcolor)
    g6.grid(row=7, column=2)
    btn6 = tk.Button(optionwindow, text="Set", bg=config.bgcolor, fg=config.fgcolor,
                     command=lambda: stcolor("textcolor", g6))
    btn6.grid(row=7, column=3)

    optionwindow.call('wm', 'attributes', '.', '-topmost', '1')
    optionwindow.mainloop()
