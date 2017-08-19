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
        get_preferences().buttonabc = self.text

        return {'FINISHED'}


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class FidgetTree(NodeTree):
    # Description string
    '''A Fidget node tree type that will show up in the node editor header'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FidgetTreeType'
    # Label for nice name display
    bl_label = 'Fidget Node Tree'
    # Icon identifier
    bl_icon = 'NODETREE'


# Fidget socket type
class FidgetSocket(NodeSocket):
    # Description string
    '''Fidget node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FidgetSocketType'
    # Label for nice name display
    bl_label = 'Fidget Node Socket'

    # Enum items list
    my_items = [
        ("DOWN", "Down", "Where your feet are"),
        ("UP", "Up", "Where your head should be"),
        ("LEFT", "Left", "Not right"),
        ("RIGHT", "Right", "Not left")
    ]

    myStringProperty = bpy.props.StringProperty(
        name="Direction",
        description="Just an example",
        default="Just an example")

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "myStringProperty", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all Fidget nodes in this tree type.
# Defines a poll function to enable instantiation.
class FidgetTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FidgetTreeType'


# Derived from the Node base type.
class FidgetNode(Node, FidgetTreeNode):
    # === Basics ===
    # Description string
    '''A Fidget node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FidgetNodeType'
    # Label for nice name display
    bl_label = 'Fidget Node'
    # Icon identifier
    bl_icon = 'SOUND'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    # myStringProperty = bpy.props.StringProperty()
    myFloatProperty = bpy.props.FloatProperty(default=3.1415926)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!

    def init(self, context):
        self.inputs.new('FidgetSocket', "input")
        #self.inputs.new('NodeSocketFloat', "World")
        #self.inputs.new('NodeSocketVector', "!")

        #self.outputs.new('NodeSocketColor', "a")
        #self.outputs.new('NodeSocketColor', "b")
        #self.outputs.new('NodeSocketFloat', "c")

    # Copy function to initialize a copied node from an existing one.
    # def copy(self, node):
        # print("Copying from node ", node)

    # Free function to clean up on removal.
    # def free(self):
        # print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label("Node settings")
        layout.operator("fidget.steabc", text="hit me").text = """
if event.type == 'LEFTMOUSE':
    if event.value == 'PRESS':
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), constraint_orientation='NORMAL')
"""

        # layout.prop(self, "myFloatProperty")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # def draw_buttons_ext(self, context, layout):
        # layout.prop(self, "myFloatProperty")
        # myStringProperty button will only be visible in the sidebar
        # layout.prop(self, "myStringProperty")

    # Optional: Fidget label
    # Explicit user label overrides this, but here we can define a label dynamically
    # def draw_label(self):
        # return "I am a Fidget node"


# ## Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py


# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FidgetTreeType'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory("SOMENODES", "Some Nodes", items=[
        # our basic node
        NodeItem("FidgetNodeType"),
        ]),
    MyNodeCategory("OTHERNODES", "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("FidgetNodeType", label="Node A", settings={
            "myStringProperty": repr("Lorem ipsum dolor sit amet"),
            "myFloatProperty": repr(1.0),
            }),
        NodeItem("FidgetNodeType", label="Node B", settings={
            "myStringProperty": repr("consectetur adipisicing elit"),
            "myFloatProperty": repr(2.0),
            }),
        ]),
    ]


def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)


def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")
