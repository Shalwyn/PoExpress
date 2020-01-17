import keyboard
import re
import functions.config as config

def alts():
    config.statsearch = 1
    keyboard.press_and_release("ctrl+c")

def watch_keyboard():
    keyboard.add_hotkey("f5", lambda: keyboard.write("\n/hideout\n"))
    keyboard.add_hotkey("alt+s", lambda: alts())
