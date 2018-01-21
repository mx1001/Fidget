import bpy
from bpy.props import *


operators_edit = [
    ("Array", "", ""),
    ("Bevel", "", ""),
    ("Subdivision", "", ""),
    ("Mirror", "", ""),
    ("Boolean", "", ""),
    ("Solidify", "", ""),
    ("Displace", "", ""),
    ("Simple Deform", "", "")]


class FidgetMenuOperatorModifiers(bpy.types.Operator):
    bl_idname = "fidget.operator_modifiers"
    bl_label = "Fidget Menu Edit Operator"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "execute menu operator"

    operator_types = EnumProperty(name="Operator Types", default={'Array'},
                                  options={"ENUM_FLAG"}, items=operators_edit)

    def execute(self, context):

        if {"Array"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Extrude'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='ARRAY')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Bevel"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Extrude Individual'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='BEVEL')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Subdivision"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Subdivide'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='SUBSURF')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Mirror"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Shade Smooth'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='MIRROR')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Boolean"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Shade Flat'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='Boolean')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Solidify"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Bridge Loops'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='SOLIDIFY')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Displace"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Inset'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='DISPLACE')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        elif {"Simple Deform"}.issubset(self.operator_types):
            bpy.ops.node.add_node(type="FidgetCommandNode", use_transform=True, settings=[{"name":"info_text", "value":"'Bevel'"}, {"name":"event_value", "value":"'PRESS'"}, {"name":"command", "value":"\"bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')\""}])
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        return {'FINISHED'}


class FidgetCustomModifiersMenu(bpy.types.Menu):
    bl_idname = "fidget.custom_modifiers_menu"
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout
        layout.operator("fidget.operator_edit", "Array").operator_types = {"Array"}
        layout.operator("fidget.operator_edit", "Bevel").operator_types = {"Bevel"}
        layout.operator("fidget.operator_edit", "Subdivision").operator_types = {"Subdivision"}
        layout.operator("fidget.operator_edit", "Mirror").operator_types = {"Mirror"}
        layout.operator("fidget.operator_edit", "Boolean").operator_types = {"Boolean"}
        layout.operator("fidget.operator_edit", "Solidify").operator_types = {"Solidify"}
        layout.operator("fidget.operator_edit", "Displace").operator_types = {"Displace"}
        layout.operator("fidget.operator_edit", "Simple Deform").operator_types = {"Simple Deform"}
