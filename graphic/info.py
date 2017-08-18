import bpy
from bgl import *
import blf
from .. utils.blender_ui import get_dpi_factor


def draw_text(text, x, y, align="LEFT", size=12, color=(1, 1, 1, 1)):
    font = 0
    dpi = 72
    blf.size(font, size, int(dpi))
    glColor4f(*color)

    if align == "LEFT":
        blf.position(font, x, y, 0)
    else:
        width, height = blf.dimensions(font, text)
        if align == "RIGHT":
            blf.position(font, x - width, y, 0)

    blf.draw(font, text)


def draw_info(self, context):
    x = self.center[0] + 50
    y = self.center[1] - 12
    draw_text("info", x, y, align="LEFT", size=12, color=(1, 1, 1, 1))
