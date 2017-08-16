import os
import bpy
from bpy.props import *


def get_preferences():
    name = get_addon_name()
    return bpy.context.user_preferences.addons[name].preferences


def get_addon_name():
    return os.path.basename(os.path.dirname(os.path.realpath(__file__)))

manipulator_modes = [
    ("MODE1", "mode1", ""),
    ("MODE2", "mode2", ""),
    ("MODE3", "mode3", "")]

settings_tabs_items = [
    ("UI", "UI", ""),
    ("PROPERTIES", "Properties", ""),
    ("INFO", "Info", ""),
    ("KEYMAP", "Keymap", "")]


class FidgetPreferences(bpy.types.AddonPreferences):
    bl_idname = get_addon_name()

    tab = EnumProperty(name="Tab", items=settings_tabs_items)
    mode = EnumProperty(name="", options={"SKIP_SAVE"}, items=manipulator_modes)

    fidget_manimulator_scale = FloatProperty(
        name="Fidget Manipulator Scale",
        description="Fidget manipulator Scale",
        default=0.7, min=0, max=10)

    fidget_manimulator_dots_scale = FloatProperty(
        name="Fidget Manipulator Dots Scale",
        description="Fidget manipulator Dots Scale",
        default=0.34, min=0, max=10)

    fidget_manimulator_radius = FloatProperty(
        name="Fidget Manipulator Radius",
        description="Fidget manipulator Radius",
        default=7, min=0, max=100)

    fidget_manimulator_rotation = IntProperty(
        name="Fidget Manipulator Rotation",
        description="Fidget manipulator Rotation",
        default=0, min=-360, max=360)

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.prop(self, "tab", expand=True)

        box = col.box()

        if self.tab == "UI":
            self.draw_ui_tab(box)
        elif self.tab == "PROPERTIES":
            self.draw_properties_tab(box)
        elif self.tab == "INFO":
            self.draw_info_tab(box)
        elif self.tab == "KEYMAP":
            self.draw_keymap_tab(box)

    def draw_ui_tab(self, layout):
        box = layout.box()

        row = box.row(align=True)
        row.prop(self, "fidget_manimulator_scale", text="Manipualtor Scale")
        row = box.row(align=True)
        row.prop(self, "fidget_manimulator_dots_scale", text="Manipulator dots scale")
        # box = layout.box()
        row = box.row(align=True)
        row.prop(self, "fidget_manimulator_radius", text="Manipulator dots radius")
        row = box.row(align=True)
        row.prop(self, "fidget_manimulator_rotation", text="Manipulator rotation")

    def draw_properties_tab(self, layout):
        box = layout.box()

    def draw_info_tab(self, layout):
        box = layout.box()

    def draw_keymap_tab(self, layout):
        box = layout.box()