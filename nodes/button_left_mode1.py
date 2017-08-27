def command(modal, context, event):
    if context.active_object is None:
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            if event.type == 'LEFTMOUSE':
                if event.value == 'PRESS':
                    bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                    bpy.ops.mesh.bevel('INVOKE_DEFAULT')
                    return {'RUNNING_MODAL'}
            self.info_text = "Bevel"

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) > 1:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        bpy.ops.hops.slash('INVOKE_DEFAULT')
                        return {'RUNNING_MODAL'}
                self.info_text = "Cslash"
            else:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        bpy.ops.wm.call_menu(name='hops.symetry_submenu')
                        return {'RUNNING_MODAL'}
                self.info_text = "Symmetry Menu"
