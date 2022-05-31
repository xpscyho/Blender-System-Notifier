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
from datetime import datetime
import bpy
import os
import locale
import subprocess
import sys
bl_info = {
    "name": "Notify",
    "author": "xpscyho",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "Global",
    "description": "Displays a system notification when render is complete on Linux and Windows based systems",
    "warning": "",
    "wiki_url": "",
    "category": "System",
}
py_exec = sys.executable
try:
    from plyer import notification
except:
    subprocess.call([py_exec, "-m", "pip", "install", "plyer",
                    "-t", os.path.join(sys.prefix, "lib", "site-packages")])
    from plyer import notification

loc = locale.getlocale()  # get current locale
locx = loc[:3]
locale.getdefaultlocale()


@bpy.app.handlers.persistent
def is_render_complete(scene):
    # get render time
    localizedPrint = {
        "es_": "Blender | Render Finalizado!",  # Espanol
        "ca_": "Blender | S´ha finalitzat la prestació!",  # Catalan
        "fr_": "Blender | Rendu terminé!",  # Frances
        "it_": "Blender | Rendering finito!",  # Italiano
        "pt_": "Blender | Renderizado concluído!",  # Portugues
        "de_": "Blender | Fertig machen!",  # Deutsch
    }
    if not locx in localizedPrint:
        localizedPrint = "Blender | Render Finished!" + \
            "\n" + str(datetime.now() - TIMER)
    else:
        localizedPrint = localizedPrint[locx] + \
            "\n" + str(datetime.now() - TIMER)
    if sys.platform == "linux":
        subprocess.call(['notify-send', '-a', 'Blender', '-u',
                        'normal', '-i', 'blender', localizedPrint])
    elif sys.platform == "win32":
        notification.notify(
            title="Blender",
            message=localizedPrint,
            app_icon=None,
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
