import os, time
from tkinter import *
from playsound import playsound
from functions.tradeget import *
from functions.pricecheck import *
from functions.keyfunctions import *
import threading

#threadmain1 = threading.Thread(target=startread())
#threadmain1.start()

#threadmain2 = threading.Thread(target=startcheckclip())
#threadmain2.start()



prev = ""
root = Tk()
#root.wm_attributes("-topmost", 1)
root.update()
root.withdraw()
DEBUG = False
i = 0
watch_keyboard()
fileName = 'C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt'
originalTime = os.path.getmtime(fileName)
while True:
    data = root.clipboard_get()
    if "Rarity: Unique" in data:

        if data != prev:
            prev = data
            builditem(data)
            t9 = threading.Thread(target=buildpricewindow)
            t9.start()
    time.sleep(0.5)

    if(os.path.getmtime(fileName) > originalTime):
        ding = open('C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt', 'r', encoding='UTF8')
        last_line = ding.readlines()[-1]
        ding.close()
        if league in last_line:
            t1 = threading.Thread(target=tradewindow)
            t1.start()
        originalTime = os.path.getmtime(fileName)
