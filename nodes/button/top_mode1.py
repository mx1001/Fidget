import bpy

def command(modal, context, event):
    if context.active_object is None:
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                bpy.ops.mesh.extrude_region_move()
                bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
                self.info_text = "Extrude"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                self.info_text = "Clean"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                self.info_text = "Clean"
            else:
                bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                self.info_text = "Clean"

        elif bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) == 2:
                bpy.ops.wm.call_menu(name='hops.bool_menu')
                self.info_text = "hardops menu"
            elif len(bpy.context.selected_objects) == 1:
                bpy.ops.wm.call_menu(name='INFO_MT_mesh_add')
                self.info_text = "Add Menu"
            else:
                bpy.ops.mesh.primitive_cube_add()
                self.info_text = "Add Cube"
