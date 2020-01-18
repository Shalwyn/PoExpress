from sys import version_info
if version_info.major == 2:
    import Tkinter
elif version_info.major == 3:
    import tkinter as tk
    from tkinter import filedialog
import win32gui
import re
import json
import requests
import functions.config as config
import fileinput
import sys
from pynput.keyboard import Key, Controller

class cWindow:
    def __init__(self):
        self._hwnd = None

    def SetAsForegroundWindow(self):
        # First, make sure all (other) always-on-top windows are hidden.
        win32gui.SetForegroundWindow(self._hwnd)

    def Maximize(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def _window_enum_callback(self, hwnd, regex):
        '''Pass to win32gui.EnumWindows() to check all open windows'''
        if self._hwnd is None and re.match(regex, str(win32gui.GetWindowText(hwnd))) is not None:
            self._hwnd = hwnd

    def find_window_regex(self, regex):

        self._hwnd = None
        win32gui.EnumWindows(self._window_enum_callback, regex)

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self._hwnd: # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def buyitem(whisp):
    regex = ".*Path of Exile.*"
    cW = cWindow()
    cW.find_window_regex(regex)
    cW.SetAsForegroundWindow()


    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type(whisp)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def searchunique(itemparse):
    global parameters
    global name

    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": itemparse,
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

    MessFrame = tk.Tk()
    MessFrame.configure(background="black")
    MessFrame.geometry('400x300+200+200')
    MessFrame.title(name)


    r = 0

    for d in result:

        if d['listing']['price'] != None:
          amount = d['listing']['price']['amount']
          currency = d['listing']['price']['currency']
          nick = d['listing']['account']['lastCharacterName']
          if 'corrupted' in d['item']:
              corrupt = d['item']['corrupted']
              w = tk.Label(MessFrame, text="price {} {} Corrupt - {}".format(amount, currency, nick), fg="Pink", bg="black").grid(row=r)
              B = tk.Button(MessFrame, text ="Buy", command=lambda: buyitem(d['listing']['whisper'])).grid(row=r, column=1)
          else:
              w = tk.Label(MessFrame, text="price {} {} - {}".format(amount, currency, nick), fg="Pink", bg="black").grid(row=r)
              B = tk.Button(MessFrame, text ="Buy", command=lambda: buyitem(d['listing']['whisper'])).grid(row=r, column=1)

          r = r + 1

    #scrollbar = tk.Scrollbar(MessFrame)
    #scrollbar.pack(side="right", fill="y")
    B = tk.Button(MessFrame, text ="Close")

    MessFrame.call('wm', 'attributes', '.', '-topmost', '1')
    MessFrame.mainloop()

def setclienttxt():
    window = tk.Tk()
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text","*.txt"),("all files","*.*")))
    for line in fileinput.input("functions\config.py", inplace=1):
        if "clienttxt" in line:

            line = line.replace(line,"clienttxt = '{}'".format(window.filename) )
        sys.stdout.write(line)
    window.destroy()

def setsound():
    window = tk.Tk()
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Wave","*.wav"),("Mp3","*.mp3"),("all files","*.*")))
    for line in fileinput.input("functions\config.py", inplace=1):
        if "soundfile" in line:

            line = line.replace(line,"soundfile = '{}'".format(window.filename) )
        sys.stdout.write(line)
    window.destroy()

def createmainmenu():
    window = tk.Tk()
    window.title("Poe Tools")
    window.configure(background="black")
    window.geometry('600x300+200+200')
    w = tk.Label(window, text="Welcome to Poe Tools", fg="Pink", bg="black").grid(row=0, column=2)
    w = tk.Label(window, text="Unique Item Search", fg="Pink", bg="black").grid(row=1, column=1)
    e = tk.Entry(window, width=30, fg="Pink", bg="black")
    e.grid(row=1, column=2)
    btn1 = tk.Button(window, text = "Search", command=lambda: searchunique(e.get()))
    btn1.grid(row=1, column=3)

    w = tk.Label(window, text="Client.txt", fg="Pink", bg="black").grid(row=2, column=1)
    f = tk.Entry(window, width=30, fg="Pink", bg="black")
    f.insert(0, config.clienttxt)
    f.grid(row=2, column=2)
    btn1 = tk.Button(window, text = "Set", command=lambda: setclienttxt())
    btn1.grid(row=2, column=3)

    w = tk.Label(window, text="Trade Sound", fg="Pink", bg="black").grid(row=3, column=1)
    g = tk.Entry(window, width=30, fg="Pink", bg="black")
    g.insert(0, config.soundfile)
    g.grid(row=3, column=2)
    btn1 = tk.Button(window, text = "Set", command=lambda: setsound())
    btn1.grid(row=3, column=3)

    window.mainloop()
