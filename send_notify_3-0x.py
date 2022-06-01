#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import os
import locale
import subprocess
import sys
from datetime import datetime
import requests
import zipfile
import pathlib
bl_info = {
    "name": "Notify",
    "author": "xpscyho",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "Global",
    "description": "Displays a system notification when render is complete",
    "warning": "",
    "wiki_url": "https://github.com/xpscyho/Notify_Blender_Render/",
    "category": "System",
}

# Mac version already has a notification system, so the addon doesn't need to register
assert sys.platform != "darwin" "macOS blender already has notifications __built in__, why install this?"
py_exec = sys.executable
script_dir = os.path.dirname(os.path.realpath(__file__))
# get site-packages path
# version = ".".join(sys.version.split('.')[:2])
# print(version)
if sys.platform == "win32":
    site_packages = str(pathlib.Path(sys.exec_prefix) /
                        "Lib" / "site-packages")
elif sys.platform == "linux":
    site_packages = str(pathlib.Path(sys.exec_prefix) /
                        "lib" / sys.version[:3] / "site-packages")
# print(site_packages)
try:
    from PIL import Image
except:
    print("\nPIL not installed in bundled Python, installing...")
    subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "pillow",
                    "-t", site_packages])
    from PIL import Image
# https://download.blender.org/branding/blender_logo_kit.zip
#
if sys.platform == "win32":
    print("Notifier | Using Windows. Notification icons need to be downloaded.")
    if not os.path.exists(script_dir+"/blender_logo_kit"):
        print("Notifier | Downloading Blender logo kit...")
        logozip = requests.get(
            "https://download.blender.org/branding/blender_logo_kit.zip", allow_redirects=True)
        open(script_dir+"/.Logo", "wb").write(logozip.content)
        with zipfile.ZipFile(script_dir + "/.Logo", "r") as zip_ref:
            zip_ref.extractall(path=script_dir)
        os.remove(script_dir+"/.Logo")
        print(
            "\nNotifier | Downloaded Blender Logo Kit, converting necessary png to ico...")
        icon = Image.open(
            script_dir+"/blender_logo_kit/square/blender_icon_128x128.png")
        icon.save(
            script_dir+"/blender_logo_kit/square/blender_icon_128x128.ico", sizes=[(128, 128)])
        print("Notifier | Converted Blender Logo Kit to ico")

# if sys.platform == "win32":
try:
    from plyer import notification
except:
    print("\nplyer not installed in bundled Python, installing...")
    subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "plyer",
                     "-t", site_packages])
    from plyer import notification

locx = locale.getlocale()[:3]  # get current locale
locale.getdefaultlocale()

# exit()


@bpy.app.handlers.persistent
def is_render_complete(scene):
    # get localization print:
    localizedPrint = {
        "es_": "¡El renderizado está hecho!\n | Duración: ",  # Espanol
        "ca_": "el renderitzat està fet!\n | Durada: ",  # Catalan
        "fr_": "le rendu est fait!\n | Durée: ",  # Frances
        "it_": "il rendering è fatto!\n | Durata: ",  # Italiano
        "pt_": "renderização está feita!\n | Duração: ",  # Portugues
        "de_": "Das rendern ist fertig!\n | Dauer: ",  # Deutsch
    }
    if not locx in localizedPrint:
        localizedPrint = "Render is done! \n | Duration: " + \
            str(datetime.now() - TIMER)
    else:
        localizedPrint = localizedPrint[locx] + str(datetime.now() - TIMER)
    # if datetime.now - TIMER > datetime(0, 0, 0, 0, 0, 30):
    print(localizedPrint)
    # Notification threshold
    if (datetime.now().timestamp() - TIMER.timestamp()) > 30:
        if sys.platform == "linux":
            subprocess.call(['notify-send', '-a', 'Blender', '-u',
                            'normal', '-i', 'blender', localizedPrint])
        elif sys.platform == "win32":
            notification.notify(
                title="Blender",
                message=localizedPrint,
                app_icon=script_dir+"/blender_logo_kit/square/blender_icon_128x128.ico",
                timeout=10
            )


classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
TIMER = None


def start_timer(scene):
    global TIMER
    TIMER = datetime.now()


def register():
    bpy.app.handlers.render_init.append(start_timer)
    bpy.app.handlers.render_complete.append(is_render_complete)


def unregister():
    bpy.app.handlers.render_complete.remove(is_render_complete)


print("Notify | Initialized")

if __name__ == '__main__':
    register()
