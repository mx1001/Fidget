import bpy
from bgl import *
import blf
from .. preferences import get_preferences
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
    x = self.center[0] + get_preferences().fidget_info_pos_x
    y = self.center[1] + get_preferences().fidget_info_pos_y
    size = get_preferences().fidget_info_font_size
    if self.button_top:
        text = "Ssharpen"
        draw_text(text, x, y, align="LEFT", size=size, color=(1, 1, 1, 1))
    elif self.button_right:
        text = "Step"
        draw_text(text, x, y, align="LEFT", size=size, color=(1, 1, 1, 1))
    elif self.button_left:
        text = "Bweight"
        draw_text(text, x, y, align="LEFT", size=size, color=(1, 1, 1, 1))
