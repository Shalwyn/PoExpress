from sys import version_info
if version_info.major == 2:
    import Tkinter
elif version_info.major == 3:
    import tkinter as tk
import os, time
from playsound import playsound
import win32gui
import re
from pynput.keyboard import Key, Controller
import threading
from datetime import datetime

league = "Metamorph"

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
        print("1")

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


def sendinvite(nicktoinvite):
    regex = ".*Path of Exile.*"
    cW = cWindow()
    cW.find_window_regex(regex)
    cW.SetAsForegroundWindow()


    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type("/invite {}".format(nicktoinvite))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def tradewindow():

    sound = "Bell.wav"
    playsound(sound)
    ding = open('C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt', 'r', encoding='UTF8')
    last_line = ding.readlines()[-1]
    ding.close()
    splitmsg = last_line.split()
    if 'wtb' in splitmsg :
        buyer = splitmsg[splitmsg.index("wtb")-1]
        del splitmsg[0:splitmsg.index("wtb")]
        buyer = buyer[:-1]
    if 'Hi,' in splitmsg :
        buyer = splitmsg[splitmsg.index("Hi,")-1]
        del splitmsg[0:splitmsg.index("Hi,")]
        buyer = buyer[:-1]
        item = splitmsg[splitmsg.index("your")+1:splitmsg.index("listed")]
        price = splitmsg[splitmsg.index("for")+1:splitmsg.index("for")+3]
        stash = splitmsg[splitmsg.index(league)+1:splitmsg.index(league)+11]

    dateTimeObj = datetime.now()
    now = dateTimeObj.strftime("%H:%M:%S")
    window = tk.Tk()
    window.title("Trade")
    window.configure(background="black")
    windowtext = " ".join(item)
    windowprice = " ".join(price)
    windowstash = " ".join(stash)
    T = tk.Text(window, height=10, width=60, bg="black", fg="pink")
    T.pack()
    T.insert(tk.END, "Nick: {} \n".format(buyer))
    T.insert(tk.END, "Item: {} \n".format(windowtext))
    T.insert(tk.END, "Price: {} \n".format(windowprice))
    T.insert(tk.END, "{} \n".format(windowstash))
    T.insert(tk.END, "{} \n".format(now))
    btn1 = tk.Button(window, text = "Invite", command=lambda: sendinvite(buyer))
    btn1.pack()

#    window.after(0, readclient())
    window.mainloop()
