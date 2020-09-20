import os
import webbrowser, time, win32api, win32gui, win32con, gd
import json, socket
import re
import requests


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

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'GDControl'
token = oauth
channel = channel

sock = socket.socket()
sock.connect((server, port))
sock.send(f'PASS {token}\n'.encode('utf-8'))
sock.send(f'NICK {nickname}\n'.encode('utf-8'))
sock.send(f'JOIN #{channel}\n'.encode('utf-8'))


def getEmotes(channelname: str):
    
    req = requests.get(f'https://api.twitch.tv/v5/users?login={channelname}', headers={'Client-ID': 'ifn3ztal79zhqkclxtmu0oljs1su98'})
    channelid = json.loads(req.text)['users'][0]['_id']

    print(channelid)
    req = requests.get(f'https://api.twitch.tv/v5/bits/actions?channel_id={channelid}', headers={'Client-ID': 'ifn3ztal79zhqkclxtmu0oljs1su98'})

    return [e['prefix'] for e in json.loads(req.text)['actions']]

rstring = '^(' + ('|').join(getEmotes(channel)) + ')\\d+$'
crstring = ':(.*?):'

def getBitAmount(chat):
    stringarray = chat.split(' ')
    bits = 0
    for s in stringarray:
        if re.match(rstring, s, re.IGNORECASE):
           bits += int(re.sub('[a-z]|[A-Z]', '', s))
    return bits

req = requests.get('https://api.twitch.tv/v5/bits/actions?channel=aeonair', headers={'Client-ID': 'ifn3ztal79zhqkclxtmu0oljs1su98'})

while True:
    resp = sock.recv(2048).decode('utf-8')
    msg = re.sub(crstring, '', resp)
    bits = getBitAmount(msg)
    if bits > 0:

        if 'click' in msg.lower():
            print('click')
            click()
        elif 'hold' in msg.lower():
            print('hold')
            hold()
        elif 'release' in msg.lower():
            print('release')
            release()
    #print(pattern.match('Cheer1'))
    