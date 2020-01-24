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
import os

if sys.platform == "linux":
    import gi

    gi.require_version("Gtk", "3.0")
    gi.require_version("Wnck", "3.0")
    from gi.repository import Gtk, Gdk, Wnck
else:
    import pygetwindow as gw
from tkinter.colorchooser import askcolor

import configparser

config = configparser.ConfigParser()
config.read('{}\config.ini'.format(os.getcwd()))

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
    buy_frame.configure(background=config['colors']['bgcolor'])
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
                                 fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=r)
                br[r] = tk.Button(buy_frame, text="Buy", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                                  command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

            else:
                wr[r] = tk.Label(buy_frame, text="price {} {} - {}".format(amount, currency, nick), fg=config['colors']['textcolor'],
                                 bg=config['colors']['bgcolor']).grid(row=r)
                br[r] = tk.Button(buy_frame, text="Buy", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                                  command=lambda whisper=whisper: buyitem(whisper)).grid(row=r, column=1)

            r = r + 1
    btn1 = tk.Button(buy_frame, text="Show on web", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: webbrowser.open(
                         "https://www.pathofexile.com/trade/search/Metamorph/" + query)).grid(row=r, column=0)
    buy_frame.call('wm', 'attributes', '.', '-topmost', '1')
    buy_frame.mainloop()


def setclienttxt():
    clientwindow = tk.Tk()
    clientwindow.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                       filetypes=(("Text", "*.txt"), ("all files", "*.*")))
    config['FILES']['clienttxt'] = clientwindow.filename
    config = configparser.ConfigParser()
    filetosave = '{}\config.ini'.format(os.getcwd())
    with open(filetosave, 'w') as configfile:

        config.write(configfile)
    clientwindow.destroy()

    clientwindow.mainloop()


def setsound():
    soundwindow = tk.Tk()
    soundwindow.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
        ("Wave", "*.wav"), ("Mp3", "*.mp3"), ("all files", "*.*")))
    config['FILES']['soundfile'] = soundwindow.filename
    filetosave = '{}\config.ini'.format(os.getcwd())
    with open(filetosave, 'w') as configfile:
        config.write(configfile)
    soundwindow.destroy()

    soundwindow.mainloop()


def setty(tytext):
    config['FILES']['tytrade'] = tytext
    filetosave = '{}\config.ini'.format(os.getcwd())
    with open(filetosave, 'w') as configfile:
        config.write(configfile)


def startopt():
    optray = threading.Thread(target=creatoptions)
    optray.start()


def stcolor(which, entry):
    (triple, hexstr) = askcolor()
    if which == "fgcolor":
        config['colors']['fgcolor'] = hexstr
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)

    elif which == "bgcolor":
        config['colors']['bgcolor'] = hexstr
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)


    elif which == "textcolor":
        config['colors']['textcolor'] = hexstr
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)

    entry.delete(0, 100)
    entry.insert(0, hexstr)


def resetcount(awakener):
    if awakener == "redeemer":
        config['awakener']['redeemer'] = str(0)
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)
        act1.config(text=config['awakener']['redeemer'])
    if awakener == "crusader":
        config['awakener']['crusader'] = str(0)
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)
        act2.config(text=config['awakener']['crusader'])
    if awakener == "warlord":
        config['awakener']['warlord'] = str(0)
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)
        act3.config(text=config['awakener']['warlord'])
    if awakener == "hunter":
        config['awakener']['hunter'] = str(0)
        filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)
        act4.config(text=config['awakener']['hunter'])


def createmainmenu():
    global act1
    global act2
    global act3
    global act4
    global e


    menuwindow = tk.Tk()
    menuwindow.title("Poe Tools")
    menuwindow.configure(background=config['colors']['bgcolor'])
    menuwindow.geometry('350x200+200+200')
    w = tk.Label(menuwindow, text="Welcome to Poe Tools", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=0, column=2)
    w = tk.Label(menuwindow, text="Unique Item Search", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=1, column=1)
    e = tk.Entry(menuwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    e.grid(row=1, column=2)
    btn1 = tk.Button(menuwindow, text="Search", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=searchwindowset).grid(
        row=1, column=3)

    at1 = tk.Label(menuwindow, text="Redeemer: ", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=2, column=1)
    act1 = tk.Label(menuwindow, text=config['awakener']['redeemer'], fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    act1.grid(row=2, column=2)
    bta1 = tk.Button(menuwindow, text="reset", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: resetcount("redeemer")).grid(row=2, column=3)

    at2 = tk.Label(menuwindow, text="Crusader: ", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=3, column=1)
    act2 = tk.Label(menuwindow, text=config['awakener']['crusader'], fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    act2.grid(row=3, column=2)
    bta2 = tk.Button(menuwindow, text="reset", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: resetcount("crusader")).grid(row=3, column=3)

    at3 = tk.Label(menuwindow, text="Warlord: ", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=4, column=1)
    act3 = tk.Label(menuwindow, text=config['awakener']['warlord'], fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    act3.grid(row=4, column=2)
    bta3 = tk.Button(menuwindow, text="reset", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: resetcount("warlord")).grid(row=4, column=3)

    at4 = tk.Label(menuwindow, text="Hunter: ", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=5, column=1)
    act4 = tk.Label(menuwindow, text=config['awakener']['hunter'], fg=config['colors']['textcolor'], bg=config['colors']['bgcolor'])
    act4.grid(row=5, column=2)
    bta4 = tk.Button(menuwindow, text="reset", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: resetcount("hunter")).grid(row=5, column=3)

    btnop = tk.Button(menuwindow, text="Options", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=startopt).grid(row=6,
                                                                                                               column=1)

    menuwindow.call('wm', 'attributes', '.', '-topmost', '1')
    menuwindow.mainloop()


def creatoptions():
    optionwindow = tk.Tk()
    optionwindow.title("Options")
    optionwindow.configure(background=config['colors']['bgcolor'])
    optionwindow.geometry('600x300+200+200')
    w = tk.Label(optionwindow, text="Client.txt", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=2, column=1)
    f = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    f.insert(0, config['FILES']['clienttxt'])
    f.grid(row=2, column=2)
    btn2 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=setclienttxt)
    btn2.grid(row=2, column=3)

    w = tk.Label(optionwindow, text="Trade Sound", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=3, column=1)
    g = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    g.insert(0, config['FILES']['soundfile'])
    g.grid(row=3, column=2)
    btn3 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=setsound)
    btn3.grid(row=3, column=3)

    w = tk.Label(optionwindow, text="Ty Text", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=4, column=1)
    g = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    g.insert(0, config['FILES']['tytrade'])
    g.grid(row=4, column=2)
    btn4 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'], command=lambda: setty(g.get()))
    btn4.grid(row=4, column=3)

    w = tk.Label(optionwindow, text="Button Foreground Color", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=5,
                                                                                                            column=1)
    g4 = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    g4.insert(0, config['colors']['fgcolor'])
    g4.grid(row=5, column=2)
    btn5 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: stcolor("fgcolor", g4))
    btn5.grid(row=5, column=3)

    w = tk.Label(optionwindow, text="Button Background Color", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=6,
                                                                                                            column=1)
    g5 = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    g5.insert(0, config['colors']['bgcolor'])
    g5.grid(row=6, column=2)
    btn5 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: stcolor("bgcolor", g5))
    btn5.grid(row=6, column=3)

    w = tk.Label(optionwindow, text="Text Color", fg=config['colors']['textcolor'], bg=config['colors']['bgcolor']).grid(row=7, column=1)
    g6 = tk.Entry(optionwindow, width=30, fg=config['colors']['fgcolor'], bg=config['colors']['bgcolor'])
    g6.insert(0, config['colors']['textcolor'])
    g6.grid(row=7, column=2)
    btn6 = tk.Button(optionwindow, text="Set", bg=config['colors']['bgcolor'], fg=config['colors']['fgcolor'],
                     command=lambda: stcolor("textcolor", g6))
    btn6.grid(row=7, column=3)

    optionwindow.call('wm', 'attributes', '.', '-topmost', '1')
    optionwindow.mainloop()
