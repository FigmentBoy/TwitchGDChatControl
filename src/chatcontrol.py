
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from twitchobserver import Observer
import webbrowser, time, win32api, win32gui, win32con, gd
from pygame import mixer
import json

win = win32gui.FindWindow(None, 'Geometry Dash')

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

mem = gd.memory.get_memory()

with Observer('GDControl', oauth) as observer:
    observer.join_channel(channel)

    print('\nBot is online! Good luck :D')
    mixer.init()

    while True:
        try:
            for event in observer.get_events():
                if event.type == 'TWITCHCHATMESSAGE':
                    if event.message.lower() == '!click' and mem.percent > 0:
                        click()
                        print('click')
                    elif event.message.lower() == '!hold' and mem.percent > 0:
                        hold()
                    elif event.message.lower()=='!release' and mem.percent > 0:
                        release()
                    elif event.message.lower() == '!rick' and event.nickname.lower() == 'figmentboy':
                        mixer.music.stop()
                        mixer.music.load('src/sounds/rick.mp3')
                        mixer.music.play()
                    elif event.message.lower() == '!bwomp' and event.nickname.lower() == 'figmentboy':
                        mixer.music.stop()
                        mixer.music.load('src/sounds/bwomp.mp3')
                        mixer.music.play()
                    elif event.message.lower() == '!knock' and event.nickname.lower() == 'figmentboy':
                        mixer.music.stop()
                        mixer.music.load('src/sounds/knock.mp3')
                        mixer.music.play()
                    elif event.message.lower() == '!stopsounds' and event.nickname.lower() == 'figmentboy':
                        mixer.music.stop()
                    elif event.message.lower().startswith('!speed') and event.nickname.lower() == 'figmentboy':
                        mem.set_speed_value(float(event.message[7:]))
                    elif event.message.lower() == '!kill' and event.nickname.lower() == 'figmentboy':
                        mem.player_kill()
                    elif event.message.lower() == '!stop' and event.nickname.lower() == 'figmentboy':
                        mem.player_freeze()
                    elif event.message.lower() == '!start' and event.nickname.lower() == 'figmentboy':
                        mem.player_unfreeze()
                    elif event.message.lower().startswith('!eval') and event.nickname.lower() == 'figmentboy':
                        try:
                            eval(event.message[6:])
                        except:
                            observer.send_message(SyntaxError, channel)
                            pass
                        


        except KeyboardInterrupt:
            observer.leave_channel(channel)
            break