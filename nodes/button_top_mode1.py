def command(modal, context, event):
    if context.active_object is None:
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.ops.mesh.extrude_region_move()
                        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
                        return {'RUNNING_MODAL'}
                self.info_text = "Extrude"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                        return {'RUNNING_MODAL'}
                self.info_text = "Clean"
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                        return {'RUNNING_MODAL'}
                self.info_text = "Clean"
            else:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                        return {'RUNNING_MODAL'}
                self.info_text = "Clean"

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) == 2:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        bpy.ops.wm.call_menu(name='hops.bool_menu')
                        return {'RUNNING_MODAL'}
                self.info_text = "hardops menu"
            elif len(bpy.context.selected_objects) == 1:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        bpy.ops.wm.call_menu(name='INFO_MT_mesh_add')
                        return {'RUNNING_MODAL'}
                self.info_text = "Add Menu"
            else:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        bpy.ops.mesh.primitive_cube_add()
                        return {'RUNNING_MODAL'}
                self.info_text = "Add Cube"
