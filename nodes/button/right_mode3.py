import bpy
from ... utils.object import get_current_selected_status

def command(self, context, event):
    if context.active_object is None:
        self.info_text = " "
        pass
    else:
        active_object, other_objects, other_object = get_current_selected_status()
        only_meshes_selected = all(object.type == "MESH" for object in bpy.context.selected_objects)
        object = context.active_object

        if object.hops.status in ("CSHARP", "CSTEP"):
            if active_object is not None and other_object is None and only_meshes_selected:
                if object.hops.is_pending_boolean:
                    self.info_text = "Slash"
                    if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                        bpy.ops.hops.slash()
                else:
                    self.info_text = "Step"
                    if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                        bpy.ops.hops.step()

        elif object.hops.status == "UNDEFINED":
            if active_object is not None and other_object is None and only_meshes_selected:
                if object.hops.is_pending_boolean:
                    self.info_text = "Slash"
                    if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                        bpy.ops.hops.slash()
                else:
                    self.info_text = "Adjust Tthick"
                    if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                        bpy.ops.hops.adjust_tthick('INVOKE_DEFAULT')
