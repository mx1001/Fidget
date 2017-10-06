import bpy
from bpy.props import *
from bpy.types import Operator, NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from . import button
from .button import reset
from .. preferences import get_preferences

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

    # TODO: add in command,script,switch node
    # info_text = StringProperty(
    #     name = "Info Text",
    #     description = "Info text to use when this button is highlighted",
    #     default = "")
    #
    # event_value = EnumProperty(
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
        # layout.prop(self, "info_text", text="")
        # layout.prop(self, "event_value", text="")

        row = layout.row(align=True)
        op = row.operator("node.fidget_update")
        op.output_id = str(self.toID())
        op.write_memory = True

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
    # limit the __locals__ and globals to bpy, context and event?
    # should be default for any command
    # toggle option for script node
# TODO: write_file and reset behavior
# TODO: info_text behavior
# TODO: event value handling
    # need to use node assigned event value and return RUNNING_MODAL on the other to prevent click-through
class build:
    error = False

    def __init__(self, operator, context, input_id="", write_memory=False, write_file=False, reset=False): # TODO: implement write_file, write_memory and reset
        self.error = False
        self.error_message = "" # TODO
        self.indentation_level = "\t"
        self.command_value = "import bpy\n\ndef command(modal, context, event):\n"

        if input_id:
            if input_id == "FidgetCommandNode":
                self.command(self.get_linked_input_node(operator.output))

            elif input_id == "FidgetScriptNode":
                self.script()

            elif input_id == "FidgetSwitchNode":
                node, bool_node, command1, command2 = self.get_switch_input_nodes(operator.input)
                self.base_switch = node
                self.switch_data = [node]
                self.switch(*self.get_switch_input_nodes(node))
                self.get_switch_nodes(node, command1, command2)

        # no links
        else:
            self.no_input_link_command(operator.output)

        if not self.error:
            self.set_output(operator, write_memory, write_file, reset)

    @staticmethod
    def node_type(node):
        types = {
            'FidgetCommandNode': 'command',
            'FidgetScriptNode': 'script',
            'FidgetSwitchNode': 'switch',
            'FidgetCompareNode': 'compare',
            'FidgetIsModeNode': 'mode'}

        return types[node.bl_idname]

    ## set ##
    def set_output(self, operator, write_memory, write_file, reset):
        self.command_value = self.command_value.expandtabs(tabsize=4)
        print("\n" + self.command_value + "\n")

        if write_memory:
            self.replace_command(operator)
        if write_file:
            pass
        if reset:
            pass

    ## replace ##
    def replace_command(self, operator):
        code = compile(self.command_value, '', 'exec')
        new_command = {}
        exec(code, new_command)
        setattr(getattr(button, "{}_{}".format(operator.output.button.lower(), operator.output.mode.lower())), "command", new_command['command'])

    ## get ##
    def get_switch_nodes(self, node, command1, command2):
        if command2:
            self.get_switch_logic(command2)

            if self.node_type(command2) != "switch":
                getattr(self, self.node_type(command2))(command2)
        else:
            self.no_input_link_command(node, index=2)

        if node == self.base_switch and len(self.switch_data) > 1:
            self.indentation_level = "\t"

        self.command_value += "{}else:\n".format(self.indentation_level)
        self.indentation_level += "\t"

        if command1:
            self.get_switch_logic(command1)

            if self.node_type(command1) != "switch":
                getattr(self, self.node_type(command1))(command1)
                self.indentation_level = self.indentation_level[:-1]
        else:
            self.no_input_link_command(node, index=1)

    def get_switch_input_nodes(self, node):
        return (node, self.get_linked_input_node(node, index=0), self.get_linked_input_node(node, index=1), self.get_linked_input_node(node, index=2))

    def get_linked_input_node(self, node, index=0):
        if len(node.inputs[index].links):
            return node.inputs[index].links[0].from_node
        else:
            return None

    def get_no_input_link_command_logic(self, node, index=0):
        return "{}{}\n".format(self.indentation_level, node.inputs[index].command)

    def get_command_logic(self, node):
        return "{}{}\n".format(self.indentation_level, node.outputs[0].command)

    def get_switch_logic(self, node):
        if self.node_type(node) == "switch" and node not in self.switch_data:

            node, bool_node, command1, command2 = self.get_switch_input_nodes(node)
            self.switch_data.append(node)
            self.switch(*self.get_switch_input_nodes(node))
            self.get_switch_nodes(node, command1, command2)

    def get_script_logic(self, node):
        pass

    def get_ismode_logic(self, node):
        logic = {
            'OBJECT': "{}if context.active_object.mode == 'OBJECT':\n".format(self.indentation_level),
            'EDIT': "{}if context.active_object.mode == 'EDIT':\n".format(self.indentation_level),
            'SCULPT': "{}if context.active_object.mode == 'SCULPT':\n".format(self.indentation_level),
            'VERTEX_PAINT': "{}if context.active_object.mode == 'VERTEX_PAINT':\n".format(self.indentation_level),
            'WEIGHT_PAINT': "{}if context.active_object.mode == 'WEIGHT_PAINT':\n".format(self.indentation_level),
            'TEXTURE_PAINT': "{}if context.active_object.mode == 'TEXTURE_PAINT':\n".format(self.indentation_level),
            'PARTICLE_EDIT': "{}if context.active_object.mode == 'PARTICLE_EDIT':\n".format(self.indentation_level)}

        return logic[node.mode]

    def get_compare_logic(self, node, a, b):
        logic = {
            'AND': lambda a, b: "{}if {} and {}:\n".format(self.indentation_level, a, b),
            'OR': lambda a, b: "{}if {} or {}:\n".format(self.indentation_level, a, b),
            'NAND': lambda a, b: "{}if not ({} and {}):\n".format(self.indentation_level, a, b),
            'NOR': lambda a, b: "{}if not ({} or {}):\n".format(self.indentation_level, a, b),
            'XOR': lambda a, b: "{}if {} ^ {}:\n".format(self.indentation_level, a, b),
            'XNOR': lambda a, b: "{}if not ({} ^ {}):\n".format(self.indentation_level, a, b)}

        return logic[node.logic](a, b)

    ## nodes ##
    def command(self, node):
        command = self.get_command_logic(node)
        self.command_value += command
        self.indentation_level = self.indentation_level[:-1]

    def script(self, node):
        pass

    def switch(self, node, bool_node, command1, command2):
        if bool_node:
            if self.node_type(bool_node) == "compare":
                self.compare(bool_node)

            elif self.node_type(bool_node) == "mode":
                self.ismode(bool_node)

        else:
            pass # update build error here

    ## bool nodes ##
    def ismode(self, node):
        logic = self.get_ismode_logic(node)
        self.command_value += logic
        self.indentation_level += "\t"

    def compare(self, node):
        # need to recursion check here; a and/or b could also be compare nodes
        bool1 = self.get_linked_input_node(node, index=0)
        bool2 = self.get_linked_input_node(node, index=1)
        logic = self.get_compare_logic(node, bool1, bool2)
        self.command_value += logic
        self.indentation_level += "\t"

    ## no links ##
    def no_input_link_command(self, node, index=0):
        command = self.get_no_input_link_command_logic(node, index)
        self.command_value += command
        self.indentation_level = self.indentation_level[:-1]

# update
class FidgetUpdate(Operator):
    bl_idname = "node.fidget_update"
    bl_label = "Update"
    bl_description = "Update this fidget button"

    output_id = StringProperty()
    write_memory = BoolProperty()
    write_file = BoolProperty()
    reset = BoolProperty()

    def execute(self, context):
        tree_name, output_name = eval(self.output_id)
        self.tree = bpy.data.node_groups[tree_name]
        self.output = self.tree.nodes[output_name]

        links = self.output.inputs[0].links

        if len(links):
            self.input = links[0].from_node

            if self.input.bl_idname in {'FidgetCommandNode', 'FidgetScriptNode', 'FidgetSwitchNode'}:
                build(self, context, self.input.bl_idname, write_memory=self.write_memory, write_file=self.write_file, reset=self.reset)

                if build.error:
                    self.report({'WARNING'}, build.error_message)
                    return {'CANCELLED'}

            # if not valid link
            else:
                self.report({'WARNING'}, "{} node is an invalid input command for {}".format(self.input.bl_label.capitalize(), self.output.bl_label.lower()))
                return {'CANCELLED'}

        # no inputs
        else:
            if self.output.inputs[0].command:
                build(self, context, write_memory=self.write_memory, write_file=self.write_file, reset=self.reset)

                if build.error:
                    self.report({'WARNING'}, build.error_message)
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
