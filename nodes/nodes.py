import bpy
from bpy.props import *
from bpy.types import Operator, NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from . import button
from .. preferences import get_preferences

class FidgetNodeTree(NodeTree):
    bl_idname = "FidgetNodeTree"
    bl_label = "Fidget Node Tree"
    bl_icon = "NODETREE"

class FidgetCommandSocket(NodeSocket):
    bl_idname = "FidgetCommandSocket"
    bl_label = "Evaluate Socket"

    display_text = StringProperty(
        name = "Display Text",
        description = "The text to display while hovering over the button",
        default = "Display Text")

    event_value = EnumProperty(
        name = "Event Value",
        description = "Execute this command on either press or release of the LMB",
        items = [
            ("PRESS", "Press", ""),
            ("RELEASE", "Release", "")],
        default = "PRESS")

    command = StringProperty(
        name = "Command",
        description = "Command to execute",
        default = "")

    def draw(self, context, layout, node, text):
        if self.is_linked and not self.is_output:
            pass
        elif node.bl_idname == "FidgetCommandNode":
            self.row(context, layout, node, specials=False)
        elif self.is_output:
            layout.label(text="Output")
        else:
            self.row(context, layout, node)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.22, 1.0)

    def row(self, context, layout, node, specials=True):
        col = layout.column() # HACK: forces row to span width
        col.scale_x = 10.0
        row = col.row(align=True)
        row.prop(self, "command", text="")
        if specials:
            op = row.operator("fidget.command_options", text="", icon="COLLAPSEMENU")
            op.tree = node.id_data.name
            op.node = node.name
            op.socket = self.name

class FidgetTreeNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "FidgetNodeTree"

class FidgetCommandNode(FidgetTreeNode, Node):
    bl_idname = "FidgetCommandNode"
    bl_label = "Command"
    bl_width_min = 150

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self.outputs[0], "display_text", text="")
        row = col.row(align=True)
        row.prop(self.outputs[0], "event_value", expand=True)

class FidgetCommandOptions(Operator):
    bl_idname = "fidget.command_options"
    bl_label = "Command Options"
    bl_description = "Adjust command options"

    tree = StringProperty()
    node = StringProperty()
    socket = StringProperty()

    def draw(self, context):
        layout = self.layout
        tree = bpy.data.node_groups[self.tree]
        node = tree.nodes[self.node]
        if node.bl_idname == "FidgetCommandNode":
            socket = node.outputs[0]
        else:
            socket = node.inputs[self.socket]
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(socket, "display_text", text="")
        row = col.row(align=True)
        row.prop(socket, "event_value", expand=True)

    def execute(self, context):

        return {'FINISHED'}

    def invoke(self, context, event):

        context.window_manager.invoke_popup(self, width=200)

        return {'RUNNING_MODAL'}

class FidgetScriptNode(FidgetTreeNode, Node):
    bl_idname = "FidgetScriptNode"
    bl_label = "Script"

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

class FidgetIsModeNode(FidgetTreeNode, Node):
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

class FidgetSwitchNode(FidgetTreeNode, Node):
    bl_idname = "FidgetSwitchNode"
    bl_label = "Switch"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Use Last")
        self.inputs.new("FidgetCommandSocket", "Command 1")
        self.inputs.new("FidgetCommandSocket", "Command 2")
        self.outputs.new("FidgetCommandSocket", "")

class FidgetCompareNode(FidgetTreeNode, Node):
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

class FidgetOutputNode(FidgetTreeNode, Node):
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

    def init(self, context):
        self.inputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "button", text="")

        row = layout.row(align=True)
        op = row.operator("fidget.update")
        op.output_id = str((self.id_data.name, self.name))
        op.write_memory = True

        # TODO: write_file and reset behavior
        # row.operator("fidget.save", text="", icon="FILE_TICK")
        # row.operator("fidget.reset", text="", icon="LOAD_FACTORY")

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


# TODO: safe compile?
    # limit the __locals__ and globals to bpy, context and event?
    # should be default for command?
    # toggle option for script
class build:
    error = False

    def __init__(self, operator, context, input_id="", write_memory=False, write_file=False, reset=False):
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

    def set_output(self, operator, write_memory, write_file, reset):
        self.command_value = self.command_value.expandtabs(tabsize=4)
        print("\n" + self.command_value + "\n")

        if write_memory:
            self.replace_command(operator)
        if write_file:
            pass
        if reset:
            pass

    def replace_command(self, operator):
        code = compile(self.command_value, '', 'exec')
        new_command = {}
        exec(code, new_command)
        setattr(getattr(button, "{}_{}".format(operator.output.button.lower(), operator.output.mode.lower())), "command", new_command['command'])

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

    def command(self, node):
        # if check the node to find the sockets, update command value with event and display text, -> function
        self.command_value += self.get_command_logic(node)
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

    def ismode(self, node):
        self.command_value += self.get_ismode_logic(node)
        self.indentation_level += "\t"

    def compare(self, node):
        # TODO: need to recursion check here; a and/or b could also be compare nodes
        bool1 = self.get_linked_input_node(node, index=0)
        bool2 = self.get_linked_input_node(node, index=1)
        self.command_value += self.get_compare_logic(node, bool1, bool2)
        self.indentation_level += "\t"

    def no_input_link_command(self, node, index=0):
        self.command_value += self.get_no_input_link_command_logic(node, index)
        self.indentation_level = self.indentation_level[:-1]

class FidgetUpdate(Operator):
    bl_idname = "fidget.update"
    bl_label = "Update"
    bl_description = "Update this fidget button"

    output_id = StringProperty()
    write_memory = BoolProperty()
    write_file = BoolProperty()
    reset = BoolProperty()

    def execute(self, context):
        try: tree_name, output_name = eval(self.output_id)
        except Exception as e:
            print(e)
            tree_name, output_name = ('NodeTree', 'Output')

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

            else:
                self.report({'WARNING'}, "{} node is an invalid input command for {}".format(self.input.bl_label.capitalize(), self.output.bl_label.lower()))
                return {'CANCELLED'}

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

class FidgetSave(Operator):
    bl_idname = "fidget.save"
    bl_label = "Save"
    bl_description = "Permantly save this node behavior as the default for this fidget button"

    def execute(self, context):
        return {'FINISHED'}

class FidgetReset(Operator):
    bl_idname = "fidget.reset"
    bl_label = "Reset"
    bl_description = "Reset this fidget button to its default behavior"

    def execute(self, context):
        return {'FINISHED'}

def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)

def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")
