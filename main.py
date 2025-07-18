from os import remove as remove
from keyboard import add_hotkey
from subprocess import run
from PIL import ImageGrab, Image
from io import BytesIO
import win32clipboard as cb
from rembg import remove as bgremove
import configparser
import pystray
from pystray import MenuItem, Icon
from time import sleep

# iconSystray = Image.open('logos/TrimShot-24x24.ico')  # To run via python terminal
iconSystray = Image.open('_internal/logos/TrimShot-24x24.ico')

config = configparser.ConfigParser()
# config.read('config.ini')  # To run via python terminal
config.read('_internal/config.ini')
hotkeyOpen = config.get('Hotkeys', 'open')
hotkeyClose = config.get('Hotkeys', 'close')


def createSystray():
    global icon

    icon = Icon("TrimShot", iconSystray, "TrimShot", menu=pystray.Menu(
        MenuItem("TrimShot", lambda icon, item: main()),
        MenuItem("Exit", closeSystray)
    ))
    
    icon.run()
    print('Systray created successfully.')


def closeSystray():
    icon.stop()
    print('Systray closed successfully.')


def takeScreenshot():
    run(['cmd', '/c', 'start', 'ms-screenclip:'])


def removeBackground():
    image = ImageGrab.grabclipboard()
    inputData = BytesIO()
    image.save(inputData, format='PNG')
    inputData.seek(0)
    outputData = bgremove(inputData.read())
    return Image.open(BytesIO(outputData))
    print('Background removed successfully.')


def clipboardCopyImage(image):
    output = BytesIO()
    image.convert("RGBA").save(output, "DIB")
    data = output.getvalue()

    cb.OpenClipboard()
    cb.EmptyClipboard()
    cb.SetClipboardData(cb.CF_DIB, data)
    sleep(1)
    cb.CloseClipboard()
    print('Image copied to clipboard successfully.')


def main():
    print('App initialized')
    old_clip = ImageGrab.grabclipboard()

    takeScreenshot()

    for _ in range(50):
        sleep(0.1)
        new_clip = ImageGrab.grabclipboard()
        if isinstance(new_clip, Image.Image):
            if old_clip is None or new_clip.tobytes() != old_clip.tobytes():
                break
    else:
        print("Timeout: No image detected.")
        return

    image = removeBackground()
    clipboardCopyImage(image)


add_hotkey(hotkeyOpen, main)
add_hotkey(hotkeyClose, closeSystray)
createSystray()

# - Eventual features:
# - Create File history option on config.ini
# - TrimShot.com
# - Win10 compatibility
# - Linux compatibility
# - Chromium extension
# - Emulate "Expand selection" photoshop's behavior
# - Exlpore possibilities of AI upscaling

# pyinstaller --noconsole --clean --onefile --add-data "config.ini;." --add-data "logos/TrimShot-24x24.ico;logos" --icon=logos/TrimShot-64x64.ico main.py