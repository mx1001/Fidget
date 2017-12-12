import bpy

def command(self, context, event):
    if context.active_object is None:
        self.info_text = " "
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                self.info_text = "Extrude"
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    bpy.ops.mesh.extrude_region_move()
                    bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                self.info_text = "Clean1"
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
            elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                self.info_text = "Clean1"
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
            else:
                self.info_text = "Clean1"
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)

        elif bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) == 2:
                self.info_text = "Bool Menu"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.wm.call_menu(name='hops.bool_menu')
            elif len(bpy.context.selected_objects) == 1:
                self.info_text = "Add Mesh"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.wm.call_menu(name='INFO_MT_mesh_add')
            else:
                self.info_text = "Add Cube"
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    bpy.ops.mesh.primitive_cube_add()
