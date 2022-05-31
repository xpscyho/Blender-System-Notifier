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
    ps1command = 'function Show-Notification {[cmdletbinding()] Param ([string]$ToastTitle,[string][parameter(ValueFromPipeline)]$ToastText);[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;$Template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);$RawXml = [xml] $Template.GetXml();($RawXml.toast.visual.binding.text|where {$_.id -eq "1"}).AppendChild($RawXml.CreateTextNode($ToastTitle)) > $null;($RawXml.toast.visual.binding.text|where {$_.id -eq "2"}).AppendChild($RawXml.CreateTextNode($ToastText)) > $null;$SerializedXml = New-Object Windows.Data.Xml.Dom.XmlDocument;$SerializedXml.LoadXml($RawXml.OuterXml);$Toast = [Windows.UI.Notifications.ToastNotification]::new($SerializedXml);$Toast.Tag = "PowerShell";$Toast.Group = "PowerShell";$Toast.ExpirationTime = [DateTimeOffset]::Now.AddMinutes(1);$Notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("PowerShell");$Notifier.Show($Toast)}'
    if sys.platform == "linux":
        subprocess.call(['notify-send', '-a', 'Blender', '-u', 'critical', '-i', 'blender', localizedPrint])
    elif sys.platform == "win32":
        os.system("powershell -command " + ps1command)
classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)

def register():
     bpy.app.handlers.render_complete.append(is_render_complete)
def unregister():
     bpy.app.handlers.render_complete.remove(is_render_complete)

if __name__ == '__main__':
    register()
