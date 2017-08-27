import bpy

def command(modal, context, event):
    if context.active_object is None:
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
            bpy.ops.mesh.bevel('INVOKE_DEFAULT')
            self.info_text = "Bevel"

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) > 1:
                bpy.ops.hops.slash('INVOKE_DEFAULT')
                self.info_text = "Cslash"
            else:
                bpy.ops.wm.call_menu(name='hops.symetry_submenu')
                self.info_text = "Symmetry Menu"
