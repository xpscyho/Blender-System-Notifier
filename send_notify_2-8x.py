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
import bpy, os, locale, subprocess, sys
from bpy.app.handlers import persistent
py_exec = sys.executable
subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
try:
    from win10toast import ToastNotifier
except ImportError:
    subprocess.call([str(py_exec), "-m", "pip", "install", "--user", "plyer"])
loc = locale.getlocale() # get current locale
locx = loc[:3]
locale.getdefaultlocale()
@persistent
def is_render_complete(scene):
    localizedPrint = {
        "es_": "Blender | Render Finalizado!", # Espanol
        "ca_": "Blender | S´ha finalitzat la prestació!", # Catalan
        "fr_": "Blender | Rendu terminé!", # Frances
        "it_": "Blender | Rendering finito!", # Italiano
        "pt_": "Blender | Renderizado concluído!", # Portugues
        "de_": "Blender | Fertig machen!", # Deutsch
    }
    if not locx in localizedPrint:
        localizedPrint = "Blender | Render Finished!"
    else:
        localizedPrint = localizedPrint[locx]
    bashCommand = f'notify-send -a "Blender" -u "critical" -i "blender" "{localizedPrint}"'
    if sys.platform == "linux":
        subprocess.check_output(['bash','-c', bashCommand])
    elif sys.platform == "win32":
        ToastNotifier().show_toast(
            "Blender",
            localizedPrint,
            duration=10,
            threaded=True
        )
classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)

def register():
     bpy.app.handlers.render_complete.append(is_render_complete)
def unregister():
     bpy.app.handlers.render_complete.remove(is_render_complete)

if __name__ == '__main__':
    register()
