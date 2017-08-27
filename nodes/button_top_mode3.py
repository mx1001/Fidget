def command(modal, context, event):
    # hardops
    if context.active_object is None:
        pass
    else:
        active_object, other_objects, other_object = get_current_selected_status()
        only_meshes_selected = all(object.type == "MESH" for object in bpy.context.selected_objects)
        object = context.active_object

        if object.hops.status in ("CSHARP", "CSTEP"):
            if active_object is not None and other_object is None and only_meshes_selected:
                if object.hops.is_pending_boolean:
                    if event.type == 'LEFTMOUSE':
                        if event.value == 'PRESS':
                            bpy.ops.hops.complex_sharpen()
                            return {'RUNNING_MODAL'}
                    self.info_text = "Csharpen"
                else:
                    if event.type == 'LEFTMOUSE':
                        if event.value == 'PRESS':
                            bpy.ops.hops.soft_sharpen()
                            return {'RUNNING_MODAL'}
                    self.info_text = "Ssharpen"

        elif object.hops.status == "UNDEFINED":
            if active_object is not None and other_object is None and only_meshes_selected:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.ops.hops.soft_sharpen()
                        return {'RUNNING_MODAL'}
                self.info_text = "Ssharpen"
