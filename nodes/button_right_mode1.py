import bpy

def command(modal, context, event):
    if context.active_object is None:
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                bpy.ops.mesh.inset('INVOKE_DEFAULT')
                self.info_text = "Inset"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
                self.info_text = "Set Sharpen"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
                self.info_text = "Set Sharpen"
            else:
                bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
                self.info_text = "Set Sharpen"

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) > 1:
                bpy.ops.hops.bool_difference('INVOKE_DEFAULT')
                self.info_text = "Bool -"
            else:
                bpy.ops.wm.call_menu(name='hops_main_menu')
                self.info_text = "Hardops Menu"
