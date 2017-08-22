import bpy
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .. preferences import get_preferences
from bpy.props import *


# Implementation of Fidget nodes from Python


class NodesUpdateButtons(bpy.types.Operator):
    bl_idname = "fidget.update_right_button"
    bl_label = "coord get"
    bl_description = "get vertex coordinates"

    top = StringProperty(
        name="abc",
        description="abc",
        default="")
    left = StringProperty(
        name="abc",
        description="abc",
        default="")
    right = StringProperty(
        name="abc",
        description="abc",
        default="")

    def execute(self, context):
        get_preferences().button_top_code_input = self.top
        get_preferences().button_left_code_input = self.left
        get_preferences().button_right_code_input = self.right

        print("")
        print(get_preferences().button_top_code_input)
        print("")
        print(get_preferences().button_left_code_input)
        print("")
        print(get_preferences().button_right_code_input)

        return {'FINISHED'}


class FidgetTree(NodeTree):
    bl_idname = 'FidgetTreeType'
    bl_label = 'Fidget Node Tree'
    bl_icon = 'NODETREE'


# Fidget socket type
class FidgetOutputSocket(NodeSocket):
    bl_idname = 'FidgetOutputSocketType'
    bl_label = 'Fidget Output Node Socket'

    code = bpy.props.StringProperty(
        name="Direction",
        description="Just an example",
        default="")

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


class FidgetStringSocket(NodeSocket):
    bl_idname = 'FidgetStringSocketType'
    bl_label = 'Fidget Node Socket'

    code = bpy.props.StringProperty(
        name="Direction",
        description="Just an example",
        default="bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')")

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "code", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


class FidgetTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FidgetTreeType'


class FidgetPressNode(Node, FidgetTreeNode):
    bl_idname = 'FidgetPressNodeType'
    bl_label = 'Fidget Press Node'
    bl_icon = 'SOUND'

    modes = [
        ("PRESS", "press", ""),
        ("RELEASE", "release", "")]

    pressorrelease = EnumProperty(name="", options={"SKIP_SAVE"}, items=modes, default="PRESS")

    releasecode = """
if event.type == 'LEFTMOUSE':
    if event.value == 'RELEASE':"""

    presscode = """
if event.type == 'LEFTMOUSE':
    if event.value == 'PRESS':"""

    def init(self, context):
        self.inputs.new('FidgetOutputSocketType', "input")
        self.outputs.new('FidgetOutputSocketType', "output")

    def update(self):
        self.code = ""

        if self.pressorrelease == "RELEASE":
            initialcode = self.releasecode
        else:
            initialcode = self.presscode

        if self.inputs[0].is_linked and self.inputs[0].links[0].is_valid:
            self.code = initialcode + "\n" + "        " + self.inputs[0].links[0].from_socket.code # + "\n" + "        " + "return {'RUNNING_MODAL'}" #return not in def soit willnot exec yet we need it...
            self.outputs[0].code = self.code

    def draw_buttons(self, context, layout):
        layout.prop(self, "pressorrelease", text="")

# bpy.ops.mesh.inset("INVOKE_DEFAULT")
# bpy.ops.mesh.inset(thickness=0.32192)
# bpy.ops.mesh.extrude_region_move("INVOKE_DEFAULT", TRANSFORM_OT_translate={"constraint_axis":(False, False, True), "constraint_orientation":'NORMAL'})


class FidgetCodeNode(Node, FidgetTreeNode):
    bl_idname = 'FidgetCodeNodeType'
    bl_label = 'Fidget Code Node'
    bl_icon = 'SOUND'

    def init(self, context):
        self.outputs.new('FidgetStringSocketType', "output")


class FidgetOutputNode(Node, FidgetTreeNode):
    bl_idname = 'FidgetOutputNodeType'
    bl_label = 'Fidget Output Node'
    bl_icon = 'SOUND'

    code_1 = bpy.props.StringProperty(
        name="Top Button",
        description="Top Button",
        default="1")

    code_2 = bpy.props.StringProperty(
        name="Right Button",
        description="Right Button",
        default="2")

    code_3 = bpy.props.StringProperty(
        name="Left Button",
        description="Left Button",
        default="3")

    def init(self, context):
        self.inputs.new('FidgetOutputSocketType', "top button")
        self.inputs.new('FidgetOutputSocketType', "right button")
        self.inputs.new('FidgetOutputSocketType', "left button")
        # print(self.inputs[0].default_value)

    def update(self):
        self.code_1 = self.inputs[0].code
        self.code_2 = self.inputs[1].code
        self.code_3 = self.inputs[2].code

        if self.inputs[0].is_linked and self.inputs[0].links[0].is_valid:
            self.code_1 = self.inputs[0].links[0].from_socket.code
        else:
            self.code_1 = " "

        if self.inputs[1].is_linked and self.inputs[1].links[0].is_valid:
            self.code_2 = self.inputs[1].links[0].from_socket.code
        else:
            self.code_2 = " "

        if self.inputs[2].is_linked and self.inputs[2].links[0].is_valid:
            self.code_3 = self.inputs[2].links[0].from_socket.code
        else:
            self.code_3 = " "

    def draw_buttons(self, context, layout):
        button = layout.operator("fidget.update_right_button", text="apply setup")
        button.top = self.code_1
        button.right = self.code_2
        button.left = self.code_3


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FidgetTreeType'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory("SOMENODES", "Some Nodes", items=[
        # our basic node
        NodeItem("FidgetOutputNodeType"),
        NodeItem("FidgetPressNodeType"),
        NodeItem("FidgetCodeNodeType")
        ]),
    MyNodeCategory("OTHERNODES", "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("FidgetOutputNodeType", label="Node A", settings={
            "StringProperty": repr("Lorem ipsum dolor sit amet"),
            "myFloatProperty": repr(1.0),
            }),
        NodeItem("FidgetOutputNodeType", label="Node B", settings={
            "myStringProperty": repr("consectetur adipisicing elit"),
            "myFloatProperty": repr(2.0),
            }),
        ]),
    ]


def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)


def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")
