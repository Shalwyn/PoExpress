import keyboard
import re
import sys
import configparser
import os

config = configparser.ConfigParser()
if sys.platform == "linux":
    config.read('{}/config.ini'.format(os.getcwd()))
else:
    config.read('{}\config.ini'.format(os.getcwd()))
if sys.platform == "linux":
    from pynput.keyboard import Key, KeyCode, Listener, Controller

    keyboard = Controller()

if sys.platform == "linux":
    # Your functions

    def function_1():
        config.statsearch = 1

        keyboard.press(Key.ctrl)
        keyboard.press(KeyCode(char='c'))
        print(config.statsearch)
        keyboard.release(Key.ctrl)
        keyboard.release(KeyCode(char='c'))




    # Currently pressed keys
    current_keys = set()

    def on_press(key):
        # When a key is pressed, add it to the set we are keeping track of and check if this set is in the dictionary
        current_keys.add(key)
        if Key.f5 in current_keys:
            current_keys.remove(key)
            keyboard.type("\n/hideout\n")

        if Key.f6 in current_keys:
            filetosave = '{}/config.ini'.format(os.getcwd())
            config['FILES']['statsearch'] = str(1)
            with open(filetosave, 'w') as configfile:
                config.write(configfile)
            current_keys.remove(key)



    def watch_keyboard():
        with Listener(on_press=on_press) as listener:
            listener.join()
else:
    def alts():
        config['FILES']['statsearch'] = str(1)
        if sys.platform == "linux":
            filetosave = '{}/config.ini'.format(os.getcwd())
        else:
            filetosave = '{}\config.ini'.format(os.getcwd())
        with open(filetosave, 'w') as configfile:
            config.write(configfile)

        keyboard.press_and_release("ctrl+c")

    def watch_keyboard():
        keyboard.add_hotkey("f5", lambda: keyboard.write("\n/hideout\n"))
        keyboard.add_hotkey("alt+s", lambda: alts())
