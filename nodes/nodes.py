import bpy
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .. preferences import get_preferences
from bpy.props import *


# Implementation of Fidget nodes from Python


class ViewportSetAbc(bpy.types.Operator):
    bl_idname = "fidget.steabc"
    bl_label = "coord get"
    bl_description = "get vertex coordinates"

    text = StringProperty(
        name="abc",
        description="abc",
        default="")

    def execute(self, context):
        get_preferences().button_right_code_input = self.text

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

    basecode = """
if event.type == 'LEFTMOUSE':
    if event.value == 'PRESS':"""

    def init(self, context):
        self.inputs.new('FidgetOutputSocketType', "input")
        self.outputs.new('FidgetOutputSocketType', "output")

    def update(self):
        self.code = ""

        if self.inputs[0].is_linked and self.inputs[0].links[0].is_valid:
            self.code = self.basecode + "\n" + "        " + self.inputs[0].links[0].from_socket.code
            self.outputs[0].code = self.code

        print(self.code)

# bpy.ops.mesh.inset("INVOKE_DEFAULT")
# bpy.ops.mesh.inset(thickness=0.32192)
#  bpy.ops.mesh.extrude_region_move("INVOKE_DEFAULT", TRANSFORM_OT_translate={"constraint_axis":(False, False, True), "constraint_orientation":'NORMAL'})


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

    code = bpy.props.StringProperty(
        name="Direction",
        description="Just an example",
        default="")

    def init(self, context):
        self.inputs.new('FidgetOutputSocketType', "input")
        # print(self.inputs[0].default_value)

    def update(self):
        print("Updating node: ", self.name)
        self.code = self.inputs[0].code

        if self.inputs[0].is_linked and self.inputs[0].links[0].is_valid:
            self.code = self.inputs[0].links[0].from_socket.code
        else:
            self.code = self.inputs[0].code

    def draw_buttons(self, context, layout):
        layout.operator("fidget.steabc", text="apply setup").text = self.code


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
