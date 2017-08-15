import bpy
from bgl import *
import math
from mathutils import Vector
from .. preferences import get_preferences
from .. utils.region import scale, inside_polygon


def draw_mode1(self, context):

    center = Vector((35.0, 21.0))

    origin = 0, 0
    value = get_preferences().fidget_manimulator_scale
    center = scale(origin, center, value)
    center = center[0] + self.old_mouse_x, center[1] + self.old_mouse_y

    radius = get_preferences().fidget_manimulator_radius
    amount = 36

    self.list = calc_circle_pints(center, radius, amount)

    polygon = []
    for x, y in zip(self.list[0], self.list[1]):
        polygon.append([x, y])

    if inside_polygon(self.mouse_x, self.mouse_y, polygon):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.is_over_mode1 = True
    else:
        self.is_over_mode1 = False
        if get_preferences().mode == "MODE1":
            glColor4f(0.29, 0.52, 1.0, 0.9)
        else:
            glColor4f(0.7, 0.7, 0.7, 0.1)

    polygon[:] = []

    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_TRIANGLE_FAN)

    for x, y in zip(self.list[0], self.list[1]):
        glVertex2f(x, y)

    glEnd()
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_BLEND)


def draw_mode2(self, context):

    center = Vector((-35.0, 21.0))

    origin = 0, 0
    value = get_preferences().fidget_manimulator_scale
    center = scale(origin, center, value)
    center = center[0] + self.old_mouse_x, center[1] + self.old_mouse_y

    radius = get_preferences().fidget_manimulator_radius
    amount = 36

    self.list = calc_circle_pints(center, radius, amount)

    polygon = []
    for x, y in zip(self.list[0], self.list[1]):
        polygon.append([x, y])

    if inside_polygon(self.mouse_x, self.mouse_y, polygon):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.is_over_mode2 = True
    else:
        self.is_over_mode2 = False
        if get_preferences().mode == "MODE2":
            glColor4f(0.29, 0.52, 1.0, 0.9)
        else:
            glColor4f(0.7, 0.7, 0.7, 0.1)

    polygon[:] = []

    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_TRIANGLE_FAN)

    for x, y in zip(self.list[0], self.list[1]):
        glVertex2f(x, y)

    glEnd()
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_BLEND)


def draw_mode3(self, context):

    center = Vector((0.0, -40.0))

    origin = 0, 0
    value = get_preferences().fidget_manimulator_scale
    center = scale(origin, center, value)
    center = center[0] + self.old_mouse_x, center[1] + self.old_mouse_y

    radius = get_preferences().fidget_manimulator_radius
    amount = 36

    self.list = calc_circle_pints(center, radius, amount)

    polygon = []
    for x, y in zip(self.list[0], self.list[1]):
        polygon.append([x, y])

    if inside_polygon(self.mouse_x, self.mouse_y, polygon):
        glColor4f(0.29, 0.52, 1.0, 0.9)
        self.is_over_mode3 = True
    else:
        self.is_over_mode3 = False
        if get_preferences().mode == "MODE3":
            glColor4f(0.29, 0.52, 1.0, 0.9)
        else:
            glColor4f(0.7, 0.7, 0.7, 0.1)

    polygon[:] = []

    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_TRIANGLE_FAN)

    for x, y in zip(self.list[0], self.list[1]):
        glVertex2f(x, y)

    glEnd()
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_BLEND)


def calc_circle_pints(center, radius, amount):
    list_dx = []
    list_dy = []

    x_offset, y_offset = center
    angle = math.radians(360 / amount)
    for i in range(amount):
        list_dx.append(math.cos(i*angle) * radius + x_offset)
        list_dy.append(math.sin(i*angle) * radius + y_offset)

    return list_dx, list_dy
