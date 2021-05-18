# Based on http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html

import sys
import traceback
import ctypes
from ctypes import wintypes
import win32con
from win32con import *

byref = ctypes.byref
user32 = ctypes.windll.user32

def handle_hotkeys(hotkey_map):
    callbacks = []
    try:
        for (vk, modifiers), callback in hotkey_map.items():
            assert user32.RegisterHotKey(None, len(callbacks), modifiers, vk)
            callbacks.append(callback)
            
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                i = msg.wParam
                if i < len(callbacks):
                    try:
                        callbacks[i]()
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback)
                        
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageA(byref(msg))
            
    finally:
        for i in range(len(callbacks)):
            user32.UnregisterHotKey(None, i)