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

        self.point_size = 6
        self.margin = 30
        self.icon_color = (0.4, 0.4, 0.4, 1.0)
        self.highlight_color = (0.29, 0.52, 1.0, 0.9)

        self.buttons = {}
        self.old_mouse_x = 0
        self.old_mouse_y = 0
        self.buttontop = False

        #bpy.types.SpaceView3D.draw_handler_add(self.viewport_buttons, (context, ), 'WINDOW', 'POST_PIXEL')
        args = (self, context)
        bpy.types.SpaceView3D.draw_handler_add(draw_manipulator, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)

        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y

        self.location_x = context.region.width * 0.5
        self.location_y = context.region.height - self.margin

        self.buttons = {
            'hops_main_menu': {
                'location': (self.location_x - self.margin, self.location_y),
                'action': "bpy.ops.wm.call_menu(name='hops_main_menu')",
                'color': self.icon_color,
                'highlight_color': self.highlight_color
            },
            'hops_helper_popup': {
                'location': (self.location_x + self.margin, self.location_y),
                'action': "bpy.ops.mesh.extrude_region_move('INVOKE_DEFAULT')",
                'color': self.icon_color,
                'highlight_color': self.highlight_color
            }
        }

        for button in self.buttons:

            button = self.buttons[button]
            active_button = button if self.is_mouse_over(*button['location']) else None

            if active_button:

                active_button['color'] = active_button['highlight_color']

            if active_button and event.type == 'LEFTMOUSE':
                if event.value == 'PRESS': # override LMB PRESS
                    # eval(active_button['action'])
                    return {'RUNNING_MODAL'}

                else:

                    eval(active_button['action'])

                    return {'PASS_THROUGH'}

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.old_mouse_x = self.mouse_x
                self.old_mouse_y = self.mouse_y

        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                if bpy.context.active_object.mode == 'EDIT':
                    if self.button_top:
                        bpy.ops.mesh.extrude_region_move()
                        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
                        return {'RUNNING_MODAL'}
                    elif self.button_right:
                        bpy.ops.mesh.inset('INVOKE_DEFAULT')
                        return {'RUNNING_MODAL'}
                    elif self.button_left:
                        bpy.ops.mesh.bevel('INVOKE_DEFAULT')
                    return {'RUNNING_MODAL'}
                
                if bpy.context.active_object.mode == 'OBJECT':
                    if self.button_top:
                         if len(bpy.context.selected_objects) > 1:
                            bpy.ops.wm.call_menu(name='hops.bool_menu')
                            return {'RUNNING_MODAL'}
                         else:
                            bpy.ops.hops.adjust_bevel('INVOKE_DEFAULT')
                            return {'RUNNING_MODAL'}
                    elif self.button_right:
                        if len(bpy.context.selected_objects) > 1:
                            bpy.ops.hops.bool_difference('INVOKE_DEFAULT')
                            return {'RUNNING_MODAL'}
                        else: 
                            bpy.ops.wm.call_menu(name='hops_main_menu')
                            return {'RUNNING_MODAL'}
                    
                    elif self.button_left:
                        bpy.ops.wm.call_menu(name='hops.reset_axis_submenu')
                        return {'RUNNING_MODAL'}
                    
        return {'PASS_THROUGH'}

    def is_mouse_over(self, x, y):

        return (self.mouse_x > x - self.margin and self.mouse_x < x + self.margin) and (self.mouse_y > y - self.margin and self.mouse_y < y + self.margin)

    def viewport_buttons(self, context):

        for button in self.buttons:

            button = self.buttons[button]

            glColor4f(*button['color'])
            glEnable(GL_BLEND)

            glPointSize(self.point_size)
            glBegin(GL_POINTS)

            glVertex2f(*button['location'])

            glEnd()
            glDisable(GL_BLEND)
