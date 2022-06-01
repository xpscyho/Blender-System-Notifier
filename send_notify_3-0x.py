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
# https://download.blender.org/branding/blender_logo_kit.zip
script_dir = os.path.dirname(os.path.realpath(__file__))
print(str(script_dir) + "/blender_logo_kit")
if not os.path.exists(script_dir+"/blender_logo_kit"):
    logozip = requests.get(
        "https://download.blender.org/branding/blender_logo_kit.zip", allow_redirects=True)
    open(script_dir+"/.Logo", "wb").write(logozip.content)
    with zipfile.ZipFile(script_dir + "/.Logo", "r") as zip_ref:
        zip_ref.extractall(path=script_dir)
    os.remove(script_dir+"/.Logo")
    print("\nDownloaded Blender Logo Kit")

py_exec = sys.executable
if sys.platform == "win32":
    try:
        from plyer import notification
    except:
        print("\nplyer not installed, installing required package")
        subprocess.call([py_exec, "-m", "pip", "install", "plyer",
                        "-t", os.path.join(sys.prefix, "lib", "site-packages")])
        from plyer import notification

locx = locale.getlocale()[:3]  # get current locale
locale.getdefaultlocale()

import bpy
@bpy.app.handlers.persistent
def is_render_complete(scene):
    # get localization print:
    localizedPrint = {
        "es_": "¡El renderizado está hecho!\n duración:",  # Espanol
        "ca_": "el renderitzat està fet!\n durada:",  # Catalan
        "fr_": "le rendu est fait!\n durée:",  # Frances
        "it_": "il rendering è fatto!\n durata:",  # Italiano
        "pt_": "renderização está feita!\n duração:",  # Portugues
        "de_": "Das rendern ist fertig!\n Dauer:",  # Deutsch
    }
    if not locx in localizedPrint:
        localizedPrint = "Render is done! \n duration:" + \
            str(datetime.now() - TIMER)
    else:
        localizedPrint = localizedPrint[locx] + str(datetime.now() - TIMER)
    # if datetime.now - TIMER > datetime(0, 0, 0, 0, 0, 30):
    if sys.platform == "linux":
        subprocess.call(['notify-send', '-a', 'Blender', '-u',
                        'normal', '-i', 'blender', localizedPrint])
    elif sys.platform == "win32":
        notification.notify(
            title="Blender",
            message=localizedPrint,
            app_icon=script_dir+"blender_logo_kit/square/blender_icon_128x128.png",
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


if __name__ == '__main__':
    register()
