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
if sys.platform == "win32":
    from win32api import *
    from win32gui import *
    import win32con
    import struct
    import time
    
    class WindowsBalloonTip:
        def __init__(self, title, msg):
            message_map = {
                    win32con.WM_DESTROY: self.OnDestroy,
            }
            # Register the Window class.
            wc = WNDCLASS()
            hinst = wc.hInstance = GetModuleHandle(None)
            wc.lpszClassName = "PythonTaskbar"
            wc.lpfnWndProc = message_map # could also specify a wndproc.
            classAtom = RegisterClass(wc)
            # Create the Window.
            style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
            self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                    0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                    0, 0, hinst, None)
            UpdateWindow(self.hwnd)
            iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            try:
                hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
            except:
                hicon = LoadIcon(0, win32con.IDI_APPLICATION)
            flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
            nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
            Shell_NotifyIcon(NIM_ADD, nid)
            Shell_NotifyIcon(NIM_MODIFY, \
                            (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                            hicon, "Balloon  tooltip",title,200,msg))
            # self.show_balloon(title, msg)
            time.sleep(10)
            DestroyWindow(self.hwnd)
        def OnDestroy(self, hwnd, msg, wparam, lparam):
            nid = (self.hwnd, 0)
            Shell_NotifyIcon(NIM_DELETE, nid)
            PostQuitMessage(0) # Terminate the app.
    def balloon_tip(title, msg):
        w=WindowsBalloonTip(msg, title)
from bpy.app.handlers import persistent
py_exec = sys.executable
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
        subprocess.call(['notify-send', '-a', 'Blender', '-u', 'critical', '-i', 'blender', localizedPrint])
    elif sys.platform == "win32":
        WindowsBalloonTip(
            title='Blender',
            msg=localizedPrint,
        )
classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)

def register():
     bpy.app.handlers.render_complete.append(is_render_complete)
def unregister():
     bpy.app.handlers.render_complete.remove(is_render_complete)

if __name__ == '__main__':
    register()
