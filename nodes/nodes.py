import bpy
from bpy.props import *
from bpy.types import Operator, NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from . import button
from .. preferences import get_preferences
from .. operators.drawing_mode import button

# node tree
class FidgetNodeTree(NodeTree):
    bl_idname = "FidgetNodeTree"
    bl_label = "Fidget Node Tree"
    bl_icon = "NODETREE"

## sockets ##

# eval socket
class FidgetCommandSocket(NodeSocket):
    bl_idname = "FidgetCommandSocket"
    bl_label = "Evaluate Socket"

    command = StringProperty(
        name = "Command",
        description = "Command to execute",
        default = "")

    def draw(self, context, layout, node, text):
        if self.is_linked and not self.is_output:
            layout.label(text=text)
        elif node.bl_idname == "FidgetCommandNode":
            row = layout.row()
            row.scale_x = 5.0 # HACK: forces row to span width
            row.prop(self, "command", text="")
        elif self.is_output:
            layout.label(text="Output")
        else:
            row = layout.row()
            row.scale_x = 5.0
            row.prop(self, "command", text="")

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.22, 1.0)

## nodes ##

# node mix-in
class FidgetTreeNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "FidgetNodeTree"

# command
class FidgetCommandNode(Node, FidgetTreeNode):
    bl_idname = "FidgetCommandNode"
    bl_label = "Command"
    bl_width_min = 150

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

# script
class FidgetScriptNode(Node, FidgetTreeNode):
    bl_idname = "FidgetScriptNode"
    bl_label = "Script"

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

# is mode
class FidgetIsModeNode(Node, FidgetTreeNode):
    bl_idname = "FidgetIsModeNode"
    bl_label = "Is Mode"

    mode = EnumProperty(
        name = "Object Mode",
        description = "Mode requirements to allow executing",
        items = [
            ("PARTICLE_EDIT", "Particle Edit", ""),
            ("TEXTURE_PAINT", "Texture Paint", ""),
            ("WEIGHT_PAINT", "Weight Paint", ""),
            ("VERTEX_PAINT", "Vertex Paint", ""),
            ("SCULPT", "Sculpt", ""),
            ("EDIT", "Edit", ""),
            ("OBJECT", "Object", "")],
        default = "OBJECT")

    def init(self, context):
        self.outputs.new("NodeSocketBool", "")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', text="")

# switch
class FidgetSwitchNode(Node, FidgetTreeNode):
    bl_idname = "FidgetSwitchNode"
    bl_label = "Switch"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Use Last")
        self.inputs.new("FidgetCommandSocket", "")
        self.inputs.new("FidgetCommandSocket", "")
        self.outputs.new("FidgetCommandSocket", "")

# compare
class FidgetCompareNode(Node, FidgetTreeNode):
    bl_idname = "FidgetCompareNode"
    bl_label = "Compare"

    logic = EnumProperty(
        name = "Logic",
        description = "Type of logic to use for comparison",
        items = [
            ("XNOR", "Xnor", "If neither or both"),
            ("XOR", "Xor", "If either"),
            ("NOR", "Nor", "If neither"),
            ("NAND", "Nand", "If not both"),
            ("OR", "Or", "If either or both"),
            ("AND", "And", "If both")],
        default = "AND")

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Boolean")
        self.inputs.new("NodeSocketBool", "Boolean")
        self.outputs.new("NodeSocketBool", "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "logic", text="")

# output
class FidgetOutputNode(Node, FidgetTreeNode):
    bl_idname = "FidgetOutputNode"
    bl_label = "Output"

    mode = EnumProperty(
        name = "Fidget Mode",
        description = "The fidget mode to target",
        items = [
            ("MODE3", "Mode 3", ""),
            ("MODE2", "Mode 2", ""),
            ("MODE1", "Mode 1", "")],
        default = "MODE1")

    button = EnumProperty(
        name = "Fidget Button",
        description = "The fidget button to target",
        items = [
            ("LEFT", "Left Button", ""),
            ("RIGHT", "Right Button", ""),
            ("TOP", "Top Button", "")],
        default = "TOP")

    lable = StringProperty(
        name = "Label Text",
        description = "Label to use when this button is highlighted",
        default = "")

    # XXX: is there a need?
    # value = EnumProperty(
    #     name = "Event Value",
    #     description = "Event value",
    #     items = [
    #         ("PRESS", "Press", ""),
    #         ("RELEASE", "Release", "")],
    #     default = "PRESS")

    def init(self, context):
        self.inputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "button", text="")
        layout.prop(self, "label", text="")
        # layout.prop(self, "value", text="")

        row = layout.row(align=True)
        op = row.operator("node.fidget_update")
        op.output_id = str(self.toID())

        # TODO
        # row.operator("node.fidget_save", text="", icon="FILE_TICK")
        # row.operator("node.fidget_reset", text="", icon="LOAD_FACTORY")

# categories
class FidgetNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "FidgetNodeTree"

node_categories = [
    FidgetNodeCategory("FIDGETINPUT", "Input", items=[
        NodeItem("FidgetCommandNode"),
        NodeItem("FidgetScriptNode")]),
    FidgetNodeCategory("FIDGETLOGIC", "Logic", items=[
        NodeItem("FidgetIsModeNode"), NodeItem("FidgetSwitchNode"), NodeItem("FidgetCompareNode")]),
    FidgetNodeCategory("FIDGETOUTPUT", "Output", items=[
        NodeItem("FidgetOutputNode")]),
    FidgetNodeCategory("LAYOUT", "Layout", items=[
        NodeItem("NodeFrame"),
        NodeItem("NodeReroute")])]


# TODO: safe compile
# limit the __locals__ and globals to bpy, context and event
# should be default for any command
# toggle option for script node
# TODO: write_file and reset behavior
# TODO: info_text behavior
class build:
    # example output
    # # switch 1
    # if istexture or ispaint: # compare, if there is not switch command 1 would be ran
    #     run last # command
    # else: # command 2 would be ran if there is not another switch
    #     # switch 2
    #     if isedit: # ismode
    #         run last # command
    #     else: # command 3 would be ran if there is not another switch
    #         # switch 3
    #         if isobject: # ismode
    #             run last # command
    #         else:
    #             run everything else # command

    # compare
    # if is_node compare is_node:
    #   run last
    # else:
    #   run first

    # switch
    # if is_node:
    #   run last
    # else:
    #   run first
    error = ""

    def __init__(self, operator, context, input_id="", write_memory=False, write_file=False, reset=False): # TODO: implement write_file, write_memory and reset
        self.error = ""
        self.indentation_level = "\t"
        self.command_value = "import bpy\n\ndef command(modal, context, event):\n\t"

        # tree_name, output_name = eval(self.output_id)
        # self.tree = bpy.data.node_groups[tree_name]
        # self.output = self.tree.nodes[output_name]
        # links = self.output.inputs[0].links
        # self.input = links[0].from_node

        if input_id:
            if input_id == "FidgetCommandNode":
                self.command(self.get_linked_node(operator.output))
            elif input_id == "FidgetScriptNode":
                pass
            elif input_id == "FidgetSwitchNode":
                bool_node = self.get_linked_node(operator.input, index=0)
                command1_node = self.get_linked_node(operator.input, index=1)
                command2_node = self.get_linked_node(operator.input, index=2)
                self.switch(bool_node, command1_node, command2_node)

        # no links
        else:
            self.no_input_link_command(operator.output)

        if not self.error:
            self.assign(operator, write_memory, write_file, reset)

    @staticmethod
    def validate_sockets(node):
        pass

    ## assign ##
    def assign(self, operator, write_memory, write_file, reset):

        print(self.command_value)
        self.command_value = self.command.expandtabs(tabsize=4)

        if write_memory:
            pass
        if write_file:
            pass
        if reset:
            pass

    ## no links ##
    def no_input_link_command(self, node):
        self.command_value += get_no_input_link_command_logic(node)
        self.indentation_level = self.indentation_level[:-1]

    ## command ##
    def command(self, node):
        self.command_value += get_command_logic(node)
        self.indentation_level = self.indentation_level[:-1]

    def script(self):
        pass

    ## logic ##
    def switch(self, bool_node, command1_node, command2_node):
        if bool_node.bl_idname == "FidgetCompareNode":
            pass

        elif bool_node.bl_idname == "FidgetIsModeNode":
            self.ismode()

            if command2_node.bl_idname == "FidgetCommandNode":
                self.command(command2_node)

            elif command2_node.bl_idname == "FidgetScriptNode":
                self.script()

            elif command2_node.bl_idname == "FidgetSwitchNode":
                pass

            if command1_node.bl_idname == "FidgetCommandNode":
                self.command(command1_node)

            elif command1_node.bl_idname == "FidgetScriptNode":
                self.script()

            elif command1_node.bl_idname == "FidgetSwitchNode":
                pass

    def ismode(self):
        self.command_value += get_ismode_logic(bool_node)
        self.indentation_level += "\t"

    def compare(self):
        pass

    ## get ##

    @staticmethod
    def get_linked_node(node, index=0):
        return node.inputs[index].links[0].from_node

    def get_no_input_link_command_logic(self, node, index=0):
        return "{}{}\n".format(self.indentation_level, node.inputs[index].command)

    def get_command_logic(self, node):
        return "{}{}\n".format(self.indentation_level, node.outputs[0].command)

    def get_ismode_logic(self, node):
        logic = {
            'OBJECT': "{}if context.active_object.mode == 'OBJECT':\n".format(self.indentation_level),
            'EDIT': "{}if context.active_object.mode == 'EDIT':\n".format(self.indentation_level),
            'SCULPT': "{}if context.active_object.mode == 'SCULPT':\n".format(self.indentation_level),
            'VERTEX_PAINT': "{}if context.active_object.mode == 'VERTEX_PAINT':\n".format(self.indentation_level),
            'WEIGHT_PAINT': "{}if context.active_object.mode == 'WEIGHT_PAINT':\n".format(self.indentation_level),
            'TEXTURE_PAINT': "{}if context.active_object.mode == 'TEXTURE_PAINT':\n".format(self.indentation_level),
            'PARTICLE_EDIT': "{}if context.active_object.mode == 'PARTICLE_EDIT':\n".format(self.indentation_level)}

        return logic[node.mode.lower()]

    def get_compare_logic(self, node, a, b):
        logic = {
            'AND': lambda a, b: "{}if {} and {}:\n".format(self.indentation_level, a, b),
            'OR': lambda a, b: "{}if {} or {}:\n".format(self.indentation_level, a, b),
            'NAND': lambda a, b: "{}if not ({} and {}):\n".format(self.indentation_level, a, b),
            'NOR': lambda a, b: "{}if not ({} or {}):\n".format(self.indentation_level, a, b),
            'XOR': lambda a, b: "{}if {} ^ {}:\n".format(self.indentation_level, a, b),
            'XNOR': lambda a, b: "{}if not ({} ^ {}):\n".format(self.indentation_level, a, b)}

        return logic[node.logic.lower()](a, b)

# update
class FidgetUpdate(Operator):
    bl_idname = "node.fidget_update"
    bl_label = "Update"
    bl_description = "Update this fidget button"

    output_id = StringProperty()

    def execute(self, context):
        tree_name, output_name = eval(self.output_id)
        self.tree = bpy.data.node_groups[tree_name]
        self.output = self.tree.nodes[output_name]

        links = self.output.inputs[0].links

        if len(self.links):
            self.input = links[0].from_node

            if self.input.bl_idname in {'FidgetCommandNode', 'FidgetScriptNode', 'FidgetSwitchNode'}:
                self.build(self, context, self.input.bl_idname, write_memory=True)

                if self.build.error:
                    self.report({'WARNING'}, self.build.error)
                    return {'CANCELLED'}

            # if not valid link
            else:
                self.report({'WARNING'}, "{} node is an invalid input command for {}".format(self.input.bl_label.capitalize(), self.output.bl_label.lower()))
                return {'CANCELLED'}

        # no inputs
        else:
            if self.output.inputs[0].command:
                self.build(self, context, self.input.bl_idname, write_memory=True)

                if self.build.error:
                    self.report({'WARNING'}, self.build.error)
                    return {'CANCELLED'}

            else:
                self.report({'WARNING'}, "Must have a command for output")
                return {'CANCELLED'}

        return {'FINISHED'}

# save
# class FidgetSave(Operator):
#     bl_idname = "node.fidget_save"
#     bl_label = "Save"
#     bl_description = "Permantly save this node behavior as the default for this fidget button"
#
#     def execute(self, context):
#         return {'FINISHED'}

# reset
# class FidgetReset(Operator):
#     bl_idname = "node.fidget_reset"
#     bl_label = "Reset"
#     bl_description = "Reset this fidget button to defaults"
#
#     def execute(self, context):
#         return {'FINISHED'}

def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)

def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")