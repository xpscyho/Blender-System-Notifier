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
import importlib
bl_info = {
    "name": "Notifier",
    "author": "xpscyho",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "Global",
    "description": "Displays a system notification when render a render completes",
    "warning": "",
    "wiki_url": "https://github.com/xpscyho/Notify_Blender_Render/",
    "category": "System",
}

# Mac version already has a notification system, so the addon doesn't need to register
assert sys.platform != "darwin" "macOS blender already has notifications __built in__, why install this?"
py_exec = sys.executable
script_dir = os.path.dirname(os.path.realpath(__file__))
# get site-packages path
# print(version)
if sys.platform == "win32":
    site_packages = str(pathlib.Path(sys.exec_prefix) /
                        "Lib" / "site-packages")
elif sys.platform == "linux":
    site_packages = str(pathlib.Path(sys.exec_prefix) /
                        "lib" / f"python{'.'.join(sys.version.split('.')[:2])}" / "site-packages")

# print(site_packages)
if sys.platform == "win32":
    invalid_packages = []
    try:
        from PIL import Image
    except:
        invalid_packages.append("pillow")
    try:
        from plyer import notification
    except:
        invalid_packages.append("plyer")
    if len(invalid_packages) > 0:
        print("Notifier | The windows version of the addon will need to install some packages:")
        for package in invalid_packages:
            print(
                f"Notifier | {package} not installed in bundled python, installing...")
            subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "--no-cache-dir", package,
                            "-t", site_packages], stderr=open(os.devnull, "w"), stdout=open(os.devnull, "w"))
        from PIL import Image
        from plyer import notification
    if not os.path.exists(script_dir+"/blender_logo_kit"):
        # https://download.blender.org/branding/blender_logo_kit.zip
        print("Notifier | Missing icon. Downloading Blender logo kit...")
        logozip = requests.get(
            "https://download.blender.org/branding/blender_logo_kit.zip", allow_redirects=True)
        open(script_dir+"/.Logo", "wb").write(logozip.content)
        with zipfile.ZipFile(script_dir + "/.Logo", "r") as zip_ref:
            zip_ref.extractall(path=script_dir)
        os.remove(script_dir+"/.Logo")
        print(
            "\nNotifier | Converting necessary png to ico...")
        icon = Image.open(
            script_dir+"/blender_logo_kit/square/blender_icon_128x128.png")
        icon.save(
            script_dir+"/blender_logo_kit/square/blender_icon_128x128.ico", sizes=[(128, 128)])

locx = locale.getlocale()[:3]  # get current locale
locale.getdefaultlocale()

# exit()


@bpy.app.handlers.persistent
def is_render_complete(scene):
    print("")
    # localization dictionary
    localizedPrint = {
        "es_": "¡El renderizado está hecho!\nDuración: ",  # Espanol
        "ca_": "el renderitzat està fet!\nDurada: ",  # Catalan
        "fr_": "le rendu est fait!\nDurée: ",  # Frances
        "it_": "il rendering è fatto!\nDurata: ",  # Italiano
        "pt_": "renderização está feita!\nDuração: ",  # Portugues
        "de_": "Das rendern ist fertig!\nDauer: ",  # Deutsch
    }
    if not locx in localizedPrint:
        localizedPrint = "Render is done!\nDuration: " + \
            str(datetime.now() - TIMER)
    else:
        localizedPrint = localizedPrint[locx] + str(datetime.now() - TIMER)
    # if datetime.now - TIMER > datetime(0, 0, 0, 0, 0, 30):
    print(localizedPrint)
    # Notification threshold
    if (datetime.now().timestamp() - TIMER.timestamp()) > bpy.context.preferences.addons[__name__].preferences.notify_threshold:
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


class NotifyPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    notify_threshold: bpy.props.IntProperty(
        name="Notification Threshold",
        description="Time in seconds to wait before displaying a notification",
        default=30,
        min=1,
        max=60
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "notify_threshold")


def start_timer(scene):
    global TIMER
    TIMER = datetime.now()


def register():
    bpy.app.handlers.render_init.append(start_timer)
    bpy.app.handlers.render_complete.append(is_render_complete)
    bpy.utils.register_class(NotifyPreferences)


def unregister():
    bpy.app.handlers.render_init.remove(start_timer)
    bpy.app.handlers.render_complete.remove(is_render_complete)
    bpy.utils.unregister_class(NotifyPreferences)


print("Notifier | Initialized")

if __name__ == '__main__':
    register()
