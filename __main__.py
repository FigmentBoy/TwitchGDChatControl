from twitchobserver import Observer
import webbrowser, time, win32api, win32gui, win32con, gd

win = win32gui.FindWindow(None, 'Geometry Dash')

def click():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def hold():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def release():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

OAUTHSITE = 'https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=ifn3ztal79zhqkclxtmu0oljs1su98&redirect_uri=https://twitchapps.com/tokengen/&scope=chat:read'

webbrowser.open_new(OAUTHSITE)

oauth = 'oauth:' + input('Enter the OAuth token here:\n')
channel = input('\nEnter your channel name here:\n').lower()

mem = gd.memory.get_memory()

with Observer('GDControl', oauth) as observer:
    observer.join_channel(channel)

    print('\nBot is online! Good luck :D')

    while True:
        try:
            for event in observer.get_events():
                if event.type == 'TWITCHCHATMESSAGE' and mem.percent > 0:
                    if event.message == '!click':
                        click()
                    elif event.message == '!hold':
                        hold()
                    elif event.message == '!release':
                        release()

        except KeyboardInterrupt:
            observer.leave_channel(channel)
            break