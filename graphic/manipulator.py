import bpy
from bgl import *
import math
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from .. utils.region import rotate, scale, inside_polygon


def draw_manipulator(self, context):

    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)

    locations_2d = [Vector((1287.5675048828125, 479.3694152832031)),
                    Vector((1290.92333984375, 478.2132568359375)), Vector((1294.163330078125, 476.3083190917969)), Vector((1297.2320556640625, 473.6871643066406)),
                    Vector((1300.076904296875, 470.3946838378906)), Vector((1302.6494140625, 466.4871826171875)), Vector((1302.5997314453125, 463.6097412109375)),
                    Vector((1302.7255859375, 460.36724853515625)), Vector((1303.2095947265625, 456.9804382324219)), Vector((1304.0435791015625, 453.5072326660156)),
                    Vector((1305.213134765625, 450.007080078125)), Vector((1306.6982421875, 446.53985595703125)), Vector((1308.4736328125, 443.1648864746094)),
                    Vector((1284.1533203125, 429.12353515625)),
                    Vector((1259.8203125, 443.1636657714844)), Vector((1261.596923828125, 446.5393371582031)), Vector((1263.0836181640625, 450.0071716308594)),
                    Vector((1264.2548828125, 453.5078125)), Vector((1265.0906982421875, 456.98138427734375)), Vector((1265.5767822265625, 460.3684387207031)),
                    Vector((1265.704833984375, 463.61102294921875)), Vector((1265.6571044921875, 466.4871826171875)), Vector((1268.2296142578125, 470.3946838378906)),
                    Vector((1271.0745849609375, 473.6871643066406)), Vector((1274.1431884765625, 476.3083190917969)), Vector((1277.3831787109375, 478.2132568359375)),
                    Vector((1280.739013671875, 479.3694152832031)),
                    Vector((1284.1533203125, 479.75701904296875))]

    locations_2d_scaled = []
    locations_2d_transed = []

    for v in locations_2d:
        v[0] = v[0] - 1284.1533203125
        v[1] = v[1] - 429.12353515625
        locations_2d_transed.append(Vector((v[0], v[1])))

    locations_2d = locations_2d_transed

    for v in locations_2d:
        origin = 0, 0
        point = v[0], v[1]
        value = 0.7
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
