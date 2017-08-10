'''
Copyright (C) 2015 masterxeon1001
masterxeon1001@gmail.com

Created by masterxeon1001 and team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "nox",
    "description": "nox",
    "author": "MX, AR",
    "version": (0, 0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    # "warning": ",
    "wiki_url": "https://masterxeon1001.com/2017/04/29/hard-ops-009-release-notes/",
    "category": "Object"}


from . import developer_utils
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

import bpy,bgl,blf
# from . registration import register_all, unregister_all


def register():
    bpy.utils.register_module(__name__)
    # register_all()
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))


def unregister():
    bpy.utils.unregister_module(__name__)
    # unregister_all()
    print("Unregistered {}".format(bl_info["name"]))
