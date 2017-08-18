import bpy
from bgl import *
import numpy as np
from .. graphic.manipulator import draw_manipulator
from .. graphic.modes import draw_mode1, draw_mode2, draw_mode3
from .. graphic.info import draw_info
from .. utils.region import region_exists, ui_contexts_under_coord, calculate_angle
from .. utils.object import get_current_selected_status
from mathutils import Vector
from .. preferences import get_preferences


def draw(self, context):

    if not (ViewportButtons.running_fidget.get(self._region) is self): return
    if self._region != context.region: return

    draw_manipulator(self, context)
    draw_mode1(self, context)
    draw_mode2(self, context)
    draw_mode3(self, context)
    draw_info(self, context)


class ViewportButtons(bpy.types.Operator):
    bl_idname = "fidget.viewport_buttons"
    bl_label = "Fidget Viewport Buttons"
    bl_description = "Draw interactive viewport buttons for hops"

    running_fidget = {}

    def invoke(self, context, event):

        if context.area.type == 'VIEW_3D':
            ViewportButtons.running_fidget = {}
            self._region_mouse = [context.region]
            self._region = context.region
            ViewportButtons.running_fidget[self._region] = self

            self.locations_2d = [Vector((3.4141845703125, 50.245880126953125)),
                                 Vector((6.77001953125, 49.0897216796875)), Vector((10.010009765625, 47.184783935546875)), Vector((13.0787353515625, 44.563629150390625)),
                                 Vector((15.923583984375, 41.271148681640625)), Vector((18.49609375, 37.3636474609375)), Vector((18.4464111328125, 34.4862060546875)),
                                 Vector((18.572265625, 31.24371337890625)), Vector((19.0562744140625, 27.856903076171875)), Vector((19.8902587890625, 24.383697509765625)),
                                 Vector((21.059814453125, 20.883544921875)), Vector((22.544921875, 17.41632080078125)), Vector((24.3203125, 14.041351318359375)),
                                 Vector((0.0, 0.0)),
                                 Vector((-24.3330078125, 14.040130615234375)), Vector((-22.556396484375, 17.415802001953125)), Vector((-21.0697021484375, 20.883636474609375)),
                                 Vector((-19.8984375, 24.38427734375)), Vector((-19.0626220703125, 27.85784912109375)), Vector((-18.5765380859375, 31.244903564453125)),
                                 Vector((-18.448486328125, 34.48748779296875)), Vector((-18.4962158203125, 37.3636474609375)), Vector((-15.9237060546875, 41.271148681640625)),
                                 Vector((-13.0787353515625, 44.563629150390625)), Vector((-10.0101318359375, 47.184783935546875)), Vector((-6.7701416015625, 49.0897216796875)),
                                 Vector((-3.414306640625, 50.245880126953125)),
                                 Vector((0.0, 50.63348388671875))]

            self.buttons = {}
            self.center = Vector((bpy.context.region.width/1.2, bpy.context.region.height/3))
            self.drag_static = Vector((self.center[0]+35.0, self.center[1]+21.0))

            self.buttontop = False
            self.manipulator_scale = 0.7
            self.manipulator_radius = 4

            self.is_over_mode1 = False
            self.is_over_mode2 = False
            self.is_over_mode3 = False

            self.drag_mode = None

            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)

            context.area.tag_redraw()
            return {'RUNNING_MODAL'}

        else:
            return {'CANCELLED'}

    def validate_region(self):
        if not (ViewportButtons.running_fidget.get(self._region) is self): return False
        return region_exists(self._region)

    def modal(self, context, event):

        try:
            if not self.validate_region():
                self.cancel(context)
                return {'CANCELLED'}

            context.area.tag_redraw()

            if event.type == 'MOUSEMOVE':
                self.mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))
                x_abs = self.mouse_pos[0] + context.region.x
                y_abs = self.mouse_pos[1] + context.region.y
                ui_contexts = list(ui_contexts_under_coord(x_abs, y_abs, context.window))
                if ui_contexts and ui_contexts[0]:
                    self._region_mouse = [uic["region"] for uic in ui_contexts]

            if not (self._region in self._region_mouse): return {'PASS_THROUGH'}

            if event.type == 'RIGHTMOUSE':
                if event.value == 'PRESS':
                    if self.is_over_mode1:
                        self.drag_static = Vector((self.center[0]+35.0, self.center[1]+21.0))
                        self.drag_mode = 'ROTATE'
                        return {'RUNNING_MODAL'}
                    elif self.is_over_mode2:
                        self.drag_static = Vector((self.center[0]-35.0, self.center[1]+21.0))
                        self.drag_mode = 'ROTATE'
                        return {'RUNNING_MODAL'}
                    elif self.is_over_mode3:
                        self.drag_static = Vector((self.center[0], self.center[1]-40.0))
                        self.drag_mode = 'ROTATE'
                        return {'RUNNING_MODAL'}
                    if self.button_top or self.button_left or self.button_right:
                        self.drag_mode = 'MOVE'
                        return {'RUNNING_MODAL'}
                elif event.value == 'RELEASE':
                    self.drag_mode = None

            elif event.type == 'LEFTMOUSE':

                if event.value == 'PRESS':
                    if self.is_over_mode1:
                        get_preferences().mode = "MODE1"
                        return {'RUNNING_MODAL'}
                    elif self.is_over_mode2:
                        get_preferences().mode = "MODE2"
                        return {'RUNNING_MODAL'}
                    elif self.is_over_mode3:
                        get_preferences().mode = "MODE3"
                        return {'RUNNING_MODAL'}

                    if get_preferences().mode == "MODE1":
                        if context.active_object is None:
                            pass
                        else:
                            if bpy.context.active_object.mode == 'EDIT':
                                if self.button_top:
                                    # Face Mode
                                    if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                                        bpy.ops.mesh.extrude_region_move()
                                        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                                    else:
                                        bpy.ops.clean1.objects('INVOKE_DEFAULT', clearsharps=False)
                                    return {'RUNNING_MODAL'}
                                elif self.button_right:
                                    # Face Mode
                                    if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                                        bpy.ops.mesh.inset('INVOKE_DEFAULT')
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        bpy.ops.hops.set_edit_sharpen('INVOKE_DEFAULT')
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
                                        pass
                                    else:
                                        pass
                                    return {'RUNNING_MODAL'}
                                elif self.button_right:
                                    if len(bpy.context.selected_objects) > 1:
                                        pass
                                    else:
                                        pass
                                    return {'RUNNING_MODAL'}
                                elif self.button_left:
                                    if len(bpy.context.selected_objects) > 1:
                                        pass
                                    else:
                                        pass
                                    return {'RUNNING_MODAL'}

                    # Hardops mode (hardcoded)
                    if get_preferences().mode == "MODE3":
                        active_object, other_objects, other_object = get_current_selected_status()
                        only_meshes_selected = all(object.type == "MESH" for object in bpy.context.selected_objects)

                        object = bpy.context.active_object

                        if len(bpy.context.selected_objects) == 1:
                            if object.hops.status in ("CSHARP", "CSTEP"):
                                if active_object is not None and other_object is None and only_meshes_selected:
                                    if object.hops.is_pending_boolean:
                                        if self.button_top:
                                            bpy.ops.hops.complex_sharpen()
                                            return {'RUNNING_MODAL'}
                                        elif self.button_left:
                                            bpy.ops.hops.adjust_bevel('INVOKE_DEFAULT')
                                            return {'RUNNING_MODAL'}
                                        elif self.button_right:
                                            bpy.ops.hops.slash()
                                            return {'RUNNING_MODAL'}
                                    else:
                                        if self.button_top:
                                            bpy.ops.hops.soft_sharpen()
                                            return {'RUNNING_MODAL'}
                                        elif self.button_left:
                                            bpy.ops.hops.adjust_bevel('INVOKE_DEFAULT')
                                            return {'RUNNING_MODAL'}
                                        elif self.button_right:
                                            bpy.ops.hops.step()
                                            return {'RUNNING_MODAL'}
                            if object.hops.status == "UNDEFINED":
                                if active_object is not None and other_object is None and only_meshes_selected:
                                    if self.button_top:
                                        bpy.ops.hops.soft_sharpen()
                                        return {'RUNNING_MODAL'}
                                    elif self.button_left:
                                        bpy.ops.hops.complex_sharpen()
                                        return {'RUNNING_MODAL'}
                                    elif self.button_right:
                                        if object.hops.is_pending_boolean:
                                            bpy.ops.hops.slash()
                                        else:
                                            bpy.ops.hops.adjust_tthick('INVOKE_DEFAULT')
                                        return {'RUNNING_MODAL'}
                        else:
                            pass

                elif event.value == 'RELEASE':

                    if get_preferences().mode == "MODE1":

                        if context.active_object is None:
                            pass
                        else:
                            if bpy.context.active_object.mode == 'EDIT':
                                if self.button_top:
                                    # Face Mode
                                    if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                                        pass
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        pass
                                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                                        pass
                                    else:
                                        pass

                            if bpy.context.active_object.mode == 'OBJECT':
                                if self.button_top:
                                    if len(bpy.context.selected_objects) == 2:
                                        bpy.ops.wm.call_menu(name='hops.bool_menu')
                                    elif len(bpy.context.selected_objects) == 1:
                                        bpy.ops.wm.call_menu(name='INFO_MT_mesh_add')
                                    else:
                                        bpy.ops.mesh.primitive_cube_add()
                                    return {'RUNNING_MODAL'}
                                elif self.button_right:
                                    if len(bpy.context.selected_objects) > 1:
                                        bpy.ops.hops.bool_difference('INVOKE_DEFAULT')
                                    else:
                                        bpy.ops.wm.call_menu(name='hops_main_menu')
                                    return {'RUNNING_MODAL'}
                                elif self.button_left:
                                    if len(bpy.context.selected_objects) > 1:
                                        bpy.ops.hops.slash('INVOKE_DEFAULT')
                                    else:
                                        bpy.ops.wm.call_menu(name='hops.symetry_submenu')
                                    return {'RUNNING_MODAL'}

            if self.drag_mode == "MOVE":
                self.center = self.mouse_pos
                self.drag_static = Vector((self.center[0]+35.0, self.center[1]+21.0))
                return {'RUNNING_MODAL'}

            elif self.drag_mode == 'ROTATE':
                self.mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))
                a = np.array([self.center.x, self.center.y])
                b = np.array([self.drag_static.x, self.drag_static.y])
                c = np.array([self.mouse_pos.x, self.mouse_pos.y])
                # create vectors
                ba = a - b
                ac = a - c
                # rotate
                base = get_preferences().fidget_manimulator_rotation_angle
                cal_angle = int(base * round(float((360 - calculate_angle(ba, ac))/base)))
                get_preferences().fidget_manimulator_rotation = cal_angle
                return {'RUNNING_MODAL'}

            if event.type == 'ESC' and event.value == 'PRESS':
                self.cancel(context)
                return {'CANCELLED'}

            return {'PASS_THROUGH'}

        except Exception as exc:
            print(exc)
            self.cancel(context)
            return {'CANCELLED'}

    def cancel(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        if ViewportButtons.running_fidget.get(self._region) is self:
            del ViewportButtons.running_fidget[self._region]
