import bpy

def command(self, context, event):
    if context.active_object is None:
        self.info_text = " "
        pass
    else:
        if bpy.context.active_object.mode == 'EDIT':
            self.info_text = "Clean and Bevel"
            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                bpy.ops.mesh.bevel('INVOKE_DEFAULT')

        if bpy.context.active_object.mode == 'OBJECT':
            if len(bpy.context.selected_objects) > 1:
                self.info_text = "Slash"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.hops.slash('INVOKE_DEFAULT')
            else:
                self.info_text = "Symmetry Menu"
                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    bpy.ops.wm.call_menu(name='hops.symetry_submenu')
