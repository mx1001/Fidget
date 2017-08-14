import bpy
from bgl import *
from .. graphic.manipulator import draw_manipulator
# from ... utils.blender_ui import get_dpi, get_dpi_factor
# from ... preferences import Hops_logo_color_cstep


class ViewportButtons(bpy.types.Operator):
    bl_idname = "nox.viewport_buttons"
    bl_label = "Viewport Buttons"
    bl_description = "Draw interactive viewport buttons for hops"

    def invoke(self, context, event):

        self.buttons = {}
        self.old_mouse_x = 0
        self.old_mouse_y = 0
        self.buttontop = False

        args = (self, context)
        bpy.types.SpaceView3D.draw_handler_add(draw_manipulator, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)

        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.old_mouse_x = self.mouse_x
                self.old_mouse_y = self.mouse_y

        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':

                if context.active_object is None:
                    pass
                else:
                    if bpy.context.active_object.mode == 'EDIT':
                        if self.button_top:
                            # Face Mode
                            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                                bpy.ops.mesh.extrude_region_move()
                                bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
                            else:
                                bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                            return {'RUNNING_MODAL'}
                        elif self.button_right:
                            # Face Mode
                            if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                                bpy.ops.mesh.inset('INVOKE_DEFAULT')
                            else:
                                bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
                            return {'RUNNING_MODAL'}
                        elif self.button_left:
                            bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                            bpy.ops.mesh.bevel('INVOKE_DEFAULT')
                        return {'RUNNING_MODAL'}

                    if bpy.context.active_object.mode == 'OBJECT':
                        if self.button_top:
                            if len(bpy.context.selected_objects) > 1:
                                bpy.ops.wm.call_menu(name='hops.bool_menu')
                                return {'RUNNING_MODAL'}
                            else:
                                bpy.ops.wm.call_menu(name='INFO_MT_mesh_add')
                                # bpy.ops.transform.resize('INVOKE_DEFAULT')
                                # bpy.ops.hops.adjust_bevel('INVOKE_DEFAULT')
                                return {'RUNNING_MODAL'}
                        elif self.button_right:
                            if len(bpy.context.selected_objects) > 1:
                                bpy.ops.hops.bool_difference('INVOKE_DEFAULT')
                                return {'RUNNING_MODAL'}
                            else:
                                bpy.ops.wm.call_menu(name='hops_main_menu')
                                return {'RUNNING_MODAL'}
                        elif self.button_left:
                            if len(bpy.context.selected_objects) > 1:
                                bpy.ops.hops.slash('INVOKE_DEFAULT')
                            else:
                                bpy.ops.wm.call_menu(name='hops.symetry_submenu')
                            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}
