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

def buildunique(itemparse):
    global parameters
    global name
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
    name = parameters['query']['name']

def buildcurrency(itemparse):
    global parameters
    global name
    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "type": itemparse.splitlines()[1],
            "stats": [{
                "type": "and",
                "filters": []
            }]
        },
        "sort": {
            "price": "asc"
        }
    }
    name = parameters['query']['type']

def buildmap(itemparse):
    global parameters
    global name
    splitmap = itemparse.splitlines()
    first = splitmap.index("--------")
    splitmap = itemparse.splitlines()[4].split()
    if "Blighted" in itemparse:
        parameters = {
            "query": {
                "status": {
                    "option": "online"
                },
                "term": itemparse.splitlines()[first-1],
                "stats": [{
                    "type": "and",
                    "filters": []
                }]
            },
            "sort": {
                "price": "asc"
            }
        }
        name = parameters['query']['term']
    else:
        parameters = {
            "query": {
                "status": {
                    "option": "online"
                },
                "type": {
                    "option": itemparse.splitlines()[first-1]
                },
                "stats": [{
                    "type": "and",
                    "filters": []
                }]
            },
            "sort": {
                "price": "asc"
            }
        }
        name = parameters['query']['type']['option']


def buildgem(itemparse):
    global parameters
    global name
    qual = 0
    if "Quality:" in itemparse.splitlines()[6].split()[0]:
        qual = itemparse.splitlines()[6].split()[1].replace('+', '')
        qual = qual.replace('%', '')
    elif "Quality:" in itemparse.splitlines()[7].split()[0]:
        qual = itemparse.splitlines()[7].split()[1].replace('+', '')
        qual = qual.replace('%', '')
    elif "Quality:" in itemparse.splitlines()[8].split()[0]:
        qual = itemparse.splitlines()[8].split()[1].replace('+', '')
        qual = qual.replace('%', '')
    elif "Quality:" in itemparse.splitlines()[9].split()[0]:
        qual = itemparse.splitlines()[9].split()[1].replace('+', '')
        qual = qual.replace('%', '')



    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "type": itemparse.splitlines()[1],
            "stats": [{
                "type": "and",
                "filters": []
            }],
            "filters": {
                "misc_filters": {
                    "filters": {
                        "gem_level": {
                            "min": itemparse.splitlines()[4].split()[1],
                            "max": itemparse.splitlines()[4].split()[1],
                        },
                        "quality": {
                            "min": qual,
                            "max": qual,
                        }

                    }
                }
            }
        },
        "sort": {
            "price": "asc"
        }
    }
    name = "{} Lvl: {} Qual: {}".format(parameters['query']['type'], itemparse.splitlines()[4].split()[1], qual)

def buildpricewindow():
    #name =

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
    MessFrame.call('wm', 'attributes', '.', '-topmost', '1')
    MessFrame.mainloop()
