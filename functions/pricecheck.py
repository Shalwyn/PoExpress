import json
import requests
import re
import tkinter
from tkinter import TclError, Tk
from pynput import keyboard
import os, time
import threading



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def builditem(itemparse):
    global parameters
    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": itemparse.splitlines()[1],
            "type": itemparse.splitlines()[2],
            "stats": [{
                "type": "and",
                "filters": []
            }]
        },
        "sort": {
            "price": "asc"
        }
    }


def buildpricewindow():
    name = parameters['query']['name']

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

    MessFrame = tkinter.Tk()
    MessFrame.configure(background="black")
    MessFrame.geometry('400x200+200+200')
    MessFrame.title(name)
    T = tkinter.Text(MessFrame, height=10, width=60, bg="black", fg="pink")
    T.pack()
    B = tkinter.Button(MessFrame, text ="Close")
    B.pack()


    for d in result:
      amount = d['listing']['price']['amount']
      currency = d['listing']['price']['currency']
      if 'corrupted' in d['item']:
        corrupt = d['item']['corrupted']
        T.insert(tkinter.END, "price {} {} Corrupted\n".format(amount, currency))
      else:
        T.insert(tkinter.END, "price {} {}\n".format(amount, currency))

    MessFrame.mainloop()
