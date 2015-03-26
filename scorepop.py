# -- coding: utf-8 --

from win32api import *
from win32gui import *
import win32con
import sys
import struct
import time
import requests
import re
import os
from time import sleep
import json

# Class
class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = { win32con.WM_DESTROY: self.OnDestroy,}

        # Register the window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = 'PythonTaskbar'
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)

        # Create the window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        UpdateWindow(self.hwnd)

        # Icons managment
        iconPathName = os.path.abspath(os.path.join( sys.path[0], 'balloontip.ico' ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, 'Tooltip')

        # Notify
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, 'Balloon Tooltip', msg, 200, title))
        # self.show_balloon(title, msg)
        time.sleep(5)

        # Destroy
        DestroyWindow(self.hwnd)
        classAtom = UnregisterClass(classAtom, hinst)
        time.sleep(5)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

# Function
def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)

def popup(title, msg):
	balloon_tip(title, msg)

def getscore():
	url = "http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/match/656493.json"
	r = requests.get(url)
	while r.status_code is not 200:
		r = requests.get(url)
	data = json.loads(r.text)
	player_status = data['match']['current_summary'].strip()
	team1_name = data['other_scores']['international'][0]['team1_name'].strip()
	team1_score = data['other_scores']['international'][0]['team1_desc'].replace('&nbsp;ov',' ov').strip()
	team2_name = data['other_scores']['international'][0]['team2_name'].strip()
	team2_score = data['other_scores']['international'][0]['team2_desc'].replace('&nbsp;ov',' ov').strip()
	if not team1_score:
		team1_score = 'Yet to bat'
	if not team2_score:
		team2_score = 'Yet to bat'
	score = str(team1_name) + ' : ' + str(team1_score) + '\n\n' + str(team2_name) + ' : ' + str(team2_score)
	player_status = re.sub(r'.*ov,','', str(player_status))
	score = score + '\nPlayer status: ' + player_status
	popup("Score Board:-", score)
	sleep(5)

# Main
if __name__ == '__main__':
    # Example
    while True:
    	getscore()
