import json
import requests
import re
import tkinter
from tkinter import TclError, Tk
from pynput import keyboard
import os, time
import threading
import functions.modlist as modlist
import functions.config as config


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

def builduniquestat(itemparse):
    links = 0
    global parameters
    global name
    splitmap = itemparse.splitlines()
    mod = {}
    value = {}

    for x in range(0, itemparse.count('\n')):
        if "Item Level:" in splitmap[x]:
            beginstat = x
            if splitmap[x-2].count('-') != 0:
                links = splitmap[x-2].count('-') + 1
            if "Allocates" in splitmap[beginstat+2]:
                beginstat = beginstat+2
            if "implicit" in splitmap[beginstat+2]:
                beginstat = beginstat+4
                break
            else:
                beginstat = x+2


    for x in range(beginstat, itemparse.count('\n')):
        if splitmap[x] == "--------":
            endstep = x
            break

    parameters = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": itemparse.splitlines()[1],
            "type": itemparse.splitlines()[2],
            "filters": {
                "socket_filters": {
                    "filters": {
                        "links": {
                            "min": links
                        }
                    }
                }
            }
        },
        "sort": {
            "price": "asc"
        },

    }


    name = "StatCheck: {} - {} Linked".format(parameters['query']['name'], links)
    parameters["query"]["stats"] = [{}]
    parameters["query"]["stats"][0]["type"] = "and"
    parameters["query"]["stats"][0]["filters"] = []

    z = 0
    for y in range(beginstat, endstep):



        mod[z] = splitmap[y].replace('+', '')
        mod[z] = re.sub("[^a-zA-Z %]+", "#", mod[z])
        #mod[z] = re.sub(r"\d+", "#", mod[z])

        if mod[z] == "#% increased Armour and Energy Shield":
            if "augmented" in itemparse:
                mod[z] = "#% increased Armour and Energy Shield (Local)"
        elif mod[z] == "#% increased Armour and Evasion":
            if "augmented" in itemparse:
                mod[z] = "#% increased Armour and Evasion (Local)"
        elif mod[z] == "#% increased Armour, Evasion and Energy Shield":
            if "augmented" in itemparse:
                mod[z] = "#% increased Armour, Evasion and Energy Shield (Local)"
        elif mod[z] == "#% increased Energy Shield":
            if "augmented" in itemparse:
                mod[z] = "#% increased Energy Shield (Local)"
        elif mod[z] == "#% increased Evasion and Energy Shield":
            if "augmented" in itemparse:
                mod[z] = "#% increased Evasion and Energy Shield (Local)"
        elif mod[z] == "#% increased Armour":
            if "augmented" in itemparse:
                mod[z] = "#% increased Armour (Local)"
        elif mod[z] == "# to Armour":
            if "augmented" in itemparse:
                mod[z] = "# to Armour (Local)"
        elif mod[z] == "# to maximum Energy Shield":
            if "augmented" in itemparse:
                mod[z] = "# to maximum Energy Shield (Local)"



        value[z] = splitmap[y].replace('+', '')
        value[z] = re.sub(r"[^0-9-]", "", value[z])

        if "Adds" in splitmap[y] and "Physical Damage" in splitmap[y] or "Chaos Damage" in splitmap[y] or "Cold Damage" in splitmap[y] or "Fire Damage" in splitmap[y] or "Lightning Damage" in splitmap[y] and "to" in splitmap[y]:
            mintomod = splitmap[y].split()
            value[z] = (int(mintomod[1]) + int(mintomod[3])) / 2


        if mod[z] in modlist.mods:

            for x in range(0, len(modlist.mods[mod[z]])):
                if "explicit" in modlist.mods[mod[z]][x]:
                    explicitstat = modlist.mods[mod[z]][x]
            min = value[z]
            parameters["query"]["stats"][0]["filters"].append({"id": explicitstat, "value": {"min": min}})
        #addfiltermods["filters"].update(addmod)
        z = z + 1

    #jprint(parameters)
    #addfilter["stats"].update(addfiltermods)
    #parameters["query"].update(addfilter)


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
