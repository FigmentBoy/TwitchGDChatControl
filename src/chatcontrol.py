import os
from twitchobserver import Observer
import webbrowser, time, win32api, win32gui, win32con, gd
import json

try:
    win = win32gui.FindWindow(None, 'Geometry Dash')
except:
    print('Please open Geometry Dash')
    exit()

def click():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def hold():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def release():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

OAUTHSITE = 'https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=ifn3ztal79zhqkclxtmu0oljs1su98&redirect_uri=https://twitchapps.com/tokengen/&scope=chat:read'

configf = open('src/config.json', 'r')
config = json.loads(configf.read())
configf.close()

if config.get('oauth') and config.get('channel'):
    oauth = config.get('oauth')
    channel = config.get('channel')
else:
    webbrowser.open_new(OAUTHSITE)
    oauth = 'oauth:' + input('Enter the OAuth token here:\n')
    channel = input('\nEnter your channel name here:\n').lower()

    config['oauth'] = oauth
    config['channel'] = channel

    configf = open('src/config.json', 'w')
    configf.write(json.dumps(config, indent=4))
    configf.close()

try:
    mem = gd.memory.get_memory()
except:
    print("Please open Geometry Dash")
    exit()

with Observer('GDControl', oauth) as observer:
    observer.join_channel(channel)

    os.system('cls')
    print('Bot is online! Good luck :D')

    while True:
        try:
            for event in observer.get_events():
                if event.type == 'TWITCHCHATMESSAGE':
                    if event.message.lower() == '!click' and mem.percent > 0:
                        click()
                    elif event.message.lower() == '!hold' and mem.percent > 0:
                        hold()
                    elif event.message.lower()=='!release' and mem.percent > 0:
                        release()
        except:
            mem = gd.memory.get_memory()
            win = win32gui.FindWindow(None, 'Geometry Dash')

