'''
Imports G-code files into Blender 2.80+ as a collection of layers which can then be animated or exported.
'''
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Import-G-code",
    "author" : "Senthur Raj",
    "description" : "Imports G-code files into Blender 2.80+ as a collection of layers.",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "File > Import-Export",
    "warning" : "",
    "category" : "Import-Export"
}

import bpy
from .preferences import IGcodePreferences, IGcodeInstaller
from .processor import ImportGcode

def menu_func_import(self, context):
    self.layout.operator(ImportGcode.bl_idname, text="G-code (.gcode)")

def register():
    bpy.utils.register_class(IGcodePreferences)
    bpy.utils.register_class(IGcodeInstaller)
    bpy.utils.register_class(ImportGcode)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(IGcodePreferences)
    bpy.utils.unregister_class(IGcodeInstaller)
    bpy.utils.unregister_class(ImportGcode)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
