import bpy
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .. preferences import get_preferences
from bpy.props import *

# fidget node tree
class FidgetNodeTree(NodeTree):
    bl_idname = "FidgetNodeTree"
    bl_label = "Fidget Node Tree"
    bl_icon = "NODETREE"

# fidget node mix-in
class FidgetTreeNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "FidgetNodeTree"

# input node
class FidgetInputNode(Node, FidgetTreeNode):
    bl_idname = "FidgetInputNode"
    bl_label = "Input"
    # bl_icon = "NONE"

    def init(self, context):
        self.inputs.new("FidgetInputNodeSocket", "hello")
        self.outputs.new("NodeSocketString", "hello")

    def draw_buttons(self, context, layout):
        layout.label("Input Value")

class FidgetInputNodeSocket(NodeSocket):
    bl_idname = "FidgetInputNodeSocket"
    bl_label = "Input Node Socket"

    value = StringProperty(
        name = "Input Value",
        description = "Command to execute",
        default = "")

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 0.8, 1.0)

# script node

    # output socket

# event node

    # input socket

    # output socket

# conditional node

    # input socket

    # output socket

# output node

    # input socket

# fidget node categories
class FidgetNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "FidgetNodeTree"

node_categories = [
    FidgetNodeCategory("FIDGETINPUT", "Input", items=[NodeItem("FidgetInputNode")]),
    # FidgetNodeCategory("INPUT", "Input", items=[NodeItem("InputNode"), NodeItem("ScriptNode")]),
    # FidgetNodeCategory("EVENT", "Event", items=[NodeItem("EventNode")]),
    # FidgetNodeCategory("CONDITION", "Condition", items=[NodeItem("ConditionNode")]),
    # FidgetNodeCategory("OUTPUT", "Output", items=[NodeItem("OutputNode")]),
]

def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)


def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")
