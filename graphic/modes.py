import bpy
from bgl import *
import math
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from .. utils.region import rotate, scale, inside_polygon


def draw_modes(self, context):

	glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)

    glColor4f(0.62, 0.5, 0.2, 0.5)

    center = 100, 100
    radius = 12
    amount = 22

    self.list_dx, self.list_dy = calc_circle_pints(center, radius, amount)

    for x, y in zip(self.list_dx, self.list_dy):
        glVertex2f(x, y)

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

