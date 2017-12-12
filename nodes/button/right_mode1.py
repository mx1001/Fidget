import bpy

def command(self, context, event):
    if context.active_object is None:
        self.info_text = " "
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                self.info_text = "Inset"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.mesh.inset('INVOKE_DEFAULT')
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                self.info_text = "Set Edit Sharpen"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                self.info_text = "Set Edit Sharpen"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
            else:
                self.info_text = "Set Edit Sharpen"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) > 1:
                self.info_text = "Bool Difference"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.hops.bool_difference('INVOKE_DEFAULT')
            else:
                self.info_text = "HOps Menu"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.wm.call_menu(name='hops_main_menu')
