import bpy
from bgl import *
import math
from mathutils import Vector
from .. preferences import get_preferences
from mathutils.geometry import tessellate_polygon
from .. utils.region import rotate, scale, inside_polygon


def draw_manipulator(self, context):

    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)

    locations_2d = self.locations_2d

    locations_2d_scaled = []

    for v in locations_2d:
        origin = 0, 0
        point = v[0], v[1]
        value = get_preferences().fidget_manimulator_scale
        px, py = scale(origin, point, value)
        locations_2d_scaled.append(Vector((px, py)))

    locations_2d = locations_2d_scaled
    location_2d_2 = []
    location_2d_3 = []

    for v in locations_2d:
        origin = 0, 0
        point = v[0], v[1]
        angle = math.radians(120)
        px, py = rotate(origin, point, angle)
        location_2d_2.append(Vector((px, py)))

    for v in locations_2d:
        origin = 0, 0
        point = v[0], v[1]
        angle = math.radians(-120)
        px, py = rotate(origin, point, angle)
        location_2d_3.append(Vector((px, py)))

    for v in locations_2d:
        v[0] = v[0] + self.old_mouse_x
        v[1] = v[1] + self.old_mouse_y
    for v in location_2d_2:
        v[0] = v[0] + self.old_mouse_x
        v[1] = v[1] + self.old_mouse_y
    for v in location_2d_3:
        v[0] = v[0] + self.old_mouse_x
        v[1] = v[1] + self.old_mouse_y

    triangles = tessellate_polygon([locations_2d])
    triangles2 = tessellate_polygon([location_2d_2])
    triangles3 = tessellate_polygon([location_2d_3])

    if inside_polygon(self.mouse_x, self.mouse_y, locations_2d):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.button_top = True
    else:
        glColor4f(0.3, 0.3, 0.3, 0.5)
        self.button_top = False
    glBegin(GL_TRIANGLES)
    for tri in triangles:
        for v_id in tri:
            v = locations_2d[v_id]
            glVertex2f(v[0], v[1])
    glEnd()

    if inside_polygon(self.mouse_x, self.mouse_y, location_2d_2):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.button_left = True
    else:
        glColor4f(0.5, 0.5, 0.5, 0.5)
        self.button_left = False
    glBegin(GL_TRIANGLES)
    for tri in triangles2:
        for v_id in tri:
            v = location_2d_2[v_id]
            glVertex2f(v[0], v[1])
    glEnd()

    if inside_polygon(self.mouse_x, self.mouse_y, location_2d_3):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.button_right = True
    else:
        glColor4f(0.7, 0.7, 0.7, 0.5)
        self.button_right = False
    glBegin(GL_TRIANGLES)
    for tri in triangles3:
        for v_id in tri:
            v = location_2d_3[v_id]
            glVertex2f(v[0], v[1])
    glEnd()

    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_BLEND)
