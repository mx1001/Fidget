import bpy
from bpy.props import *

operators = [
    ("EXTRUDE", "", ""),
    ("TRANSFORM", "", ""),
    ("TRANSFORM_X", "", ""),
    ("TRANSFORM_Y", "", ""),
    ("TRANSFORM_Z", "", ""),
    ("TRANSFORM_N", "", ""),
    ("RED_BOX", "", ""),
    ("YELLOW_BOX", "", ""),
    ("PURPLE_BOX", "", ""),
    ("GRAY_BOX", "", ""),
    ("BLUE_BOX", "", "")]


class FidgetMenuOperator(bpy.types.Operator):
    bl_idname = "fidget.operator"
    bl_label = "Fidget Menu Operator"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "execute menu operator"

    operator_types = EnumProperty(name="Operator Types", default={'EXTRUDE'},
                                  options={"ENUM_FLAG"}, items=operators)

    def execute(self, context):

        if {"TRANSFORM"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Transform'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.transform.translate('INVOKE_DEFAULT')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"EXTRUDE"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Extrude'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.mesh.extrude_region_move('INVOKE_DEFAULT')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"TRANSFORM_X"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Transform x'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(True, False, False))\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"TRANSFORM_Y"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Transform y'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, True, False))\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"TRANSFORM_Z"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Transform z'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True))\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"RED_BOX"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Red Box'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.boxcutter.invoke_operators('INVOKE_DEFAULT', mode='CUT')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"YELLOW_BOX"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Yellow Box'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.boxcutter.invoke_operators('INVOKE_DEFAULT', mode='SLICE')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"PURPLE_BOX"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Purple Box'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.boxcutter.invoke_operators('INVOKE_DEFAULT', mode='PANEL')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        return {'FINISHED'}


class FidgetCustomMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_menu"
    bl_label = "Library"

    def draw(self, context):
        layout = self.layout
        layout.menu("fidget.custom_object_menu", text="Object Mode Operators")
        layout.menu("fidget.custom_edit_menu", text="Edit Mode Operators")
        layout.menu("fidget.custom_bc_menu", text="BoxCutter Operators")
        layout.menu("fidget.custom_hops_menu", text="Hardops Operators")


class FidgetCustomObjectMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_object_menu"
    bl_label = "Object"

    def draw(self, context):
        layout = self.layout
        layout.operator("fidget.operator", "Transform").operator_types = {"TRANSFORM"}
        layout.operator("fidget.operator", "Transform x").operator_types = {"TRANSFORM_X"}
        layout.operator("fidget.operator", "Transform y").operator_types = {"TRANSFORM_Y"}
        layout.operator("fidget.operator", "Transform z").operator_types = {"TRANSFORM_Z"}


class FidgetCustomEditMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_edit_menu"
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout
        layout.operator("fidget.operator", "Extrude").operator_types = {"EXTRUDE"}


class FidgetCustomBCMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_bc_menu"
    bl_label = "BC"

    def draw(self, context):
        layout = self.layout
        layout.operator("fidget.operator", "Red Box").operator_types = {"RED_BOX"}
        layout.operator("fidget.operator", "Yellow Box").operator_types = {"YELLOW_BOX"}
        layout.operator("fidget.operator", "Purple Box").operator_types = {"PURPLE_BOX"}


class FidgetCustomHopsMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_hops_menu"
    bl_label = "Hops"

    def draw(self, context):
        layout = self.layout
