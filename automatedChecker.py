# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 15:30:43 2017

@author: Nick
"""

from ctypes import Structure, windll, c_uint, sizeof, byref
import time
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def logout_loop(controller):
    sentinel = 0
    #print("Thread Started")
    while(sentinel==0):
        time.sleep(10)
        timeIdle = get_idle_duration()
        if(timeIdle>=900):
            controller.show_frame("Login")
            sentinel=1
    return 1