import keyboard
import re

def watch_keyboard():
    keyboard.add_hotkey("f5", lambda: keyboard.write("\n/hideout\n"))

    keyboard.add_hotkey("alt+d", lambda: keyboard.press_and_release("ctrl+c"))
