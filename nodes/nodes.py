import traceback

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

    info_text = StringProperty(
        name = "Info Text",
        description = "The text to display while hovering over the button",
        default = "Info Text")

    event_value = EnumProperty(
        name = "Event Value",
        description = "Execute this command on either press or release of the LMB",
        items = [
            ("PRESS", "Press", ""),
            ("RELEASE", "Release", "Most things behave better with this value")],
        default = "RELEASE")

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
        col.scale_x = 10
        row = col.row(align=True)
        row.prop(self, "command", text="")
        if specials:
            op = row.operator("fidget.command_options", text="", icon="COLLAPSEMENU")
            op.tree = node.id_data.name
            op.node = node.name
            op.socket = self.name

class FidgetBoolSocket(NodeSocket):
    bl_idname = "FidgetBoolSocket"
    bl_label = "Bool Socket"

    value = BoolProperty(
        name = "Value",
        description = "The value of this boolean socket",
        default = True)

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

    statement = StringProperty(
        name = "Statement",
        description = "Statement to evaluate",
        default = "")

    def draw(self, context, layout, node, text):
        col = layout.column()
        col.scale_x = 10
        row = col.row(align=True)

        if node.bl_idname == "FidgetSwitchNode":
            row.label(text=self.name)
        elif node.bl_idname == "FidgetCompareNode":
            if self.is_output:
                row.prop(self, "logic", text="")
            else:
                row.label(text="Boolean")
        elif node.bl_idname == "FidgetActiveObjectNode":
            if self.name == "Object":
                sub = row.row()
                sub.prop(self, "value", text="")
                row.label(text="{} active object".format("Is" if self.value else "Isn't"))
        elif node.bl_idname == "FidgetObjectModeNode":
            row.prop(self, "mode", text="")
        elif node.bl_idname == "FidgetStatementNode":
            row.prop(self, "statement", text="")

    def draw_color(self, context, node):
        return (0.698, 0.651, 0.188, 1.0)

class FidgetTreeNode:
    bl_width_min = 150

    @classmethod
    def poll(build, ntree):
        return ntree.bl_idname == "FidgetNodeTree"

class FidgetCommandNode(FidgetTreeNode, Node):
    bl_idname = "FidgetCommandNode"
    bl_label = "Command"

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self.outputs[0], "info_text", text="")
        row = col.row(align=True)
        row.prop(self.outputs[0], "event_value", expand=True)

class FidgetNodeOperators:

    tree = StringProperty()
    node = StringProperty()
    socket = StringProperty()

    @classmethod
    def poll(build, context):
        return context.area.type == "NODE_EDITOR" and context.space_data.tree_type == "FidgetNodeTree"

    @staticmethod
    def get_count_word(integer):
        convert = [
            'First',
            'Second',
            'Third',
            'Fourth',
            'Fifth',
            'Sixth',
            'Seventh',
            'Eighth',
            'Ninth',
            'Tenth']

        return convert[integer]

class FidgetCommandOptions(FidgetNodeOperators, Operator):
    bl_idname = "fidget.command_options"
    bl_label = "Command Options"
    bl_description = "Adjust command options"

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
        row.prop(socket, "info_text", text="")
        row = col.row(align=True)
        row.prop(socket, "event_value", expand=True)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):

        context.window_manager.invoke_popup(self, width=200)

        return {'RUNNING_MODAL'}

class FidgetCommandAdd(FidgetNodeOperators, Operator):
    bl_idname = "fidget.command_add"
    bl_label = "Add Command"
    bl_description = "Add a command and bool input socket pair to this node"

    def execute(self, context):
        tree = bpy.data.node_groups[self.tree]
        node = tree.nodes[self.node]

        split = len(node.inputs)//2
        bool_count = len(node.inputs[:split])
        node.inputs.new("FidgetBoolSocket", "Use {}".format(self.get_count_word(bool_count)))
        node.inputs.move(len(node.inputs)-1, bool_count)
        command_count = len(node.inputs[split:])
        node.inputs.new("FidgetCommandSocket", "Command {}".format(command_count))
        return {'FINISHED'}

class FidgetCommandRemove(FidgetNodeOperators, Operator):
    bl_idname = "fidget.command_remove"
    bl_label = "Remove Command"
    bl_description = "Remove the last command and bool input socket pair from this node"

    def execute(self, context):
        tree = bpy.data.node_groups[self.tree]
        node = tree.nodes[self.node]

        bool_index = len(node.inputs[:len(node.inputs)//2])-1
        node.inputs.remove(node.inputs[bool_index])
        node.inputs.remove(node.inputs[-1])
        return {'FINISHED'}

class FidgetSwitchNode(FidgetTreeNode, Node):
    bl_idname = "FidgetSwitchNode"
    bl_label = "Switch"

    def init(self, context):
        self.inputs.new("FidgetBoolSocket", "Use First")
        self.inputs.new("FidgetCommandSocket", "Command 1")
        self.inputs.new("FidgetCommandSocket", "Command 2")
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator() # give us some space!

        col = layout.column()
        col.scale_x = 10

        split = col.split(align=True)

        sub = split.column(align=True)
        sub.scale_y = 1.25
        sub.enabled = len(self.inputs) > 3
        op = sub.operator("fidget.command_remove", text="", icon="ZOOMOUT")
        op.tree = self.id_data.name
        op.node = self.name

        sub = split.column(align=True)
        sub.scale_y = 1.25
        sub.enabled = len(self.inputs) < 21
        op = sub.operator("fidget.command_add", text="", icon="ZOOMIN")
        op.tree = self.id_data.name
        op.node = self.name

class FidgetScriptNode(FidgetTreeNode, Node):
    bl_idname = "FidgetScriptNode"
    bl_label = "Script"

    def init(self, context):
        self.outputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

class FidgetCompareNode(FidgetTreeNode, Node):
    bl_idname = "FidgetCompareNode"
    bl_label = "Compare"

    def init(self, context):
        self.outputs.new("FidgetBoolSocket", "")
        self.inputs.new("FidgetBoolSocket", "Boolean")
        self.inputs.new("FidgetBoolSocket", "Boolean")

class FidgetObjectModeNode(FidgetTreeNode, Node):
    bl_idname = "FidgetObjectModeNode"
    bl_label = "Object Mode"

    def init(self, context):
        self.outputs.new("FidgetBoolSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

class FidgetActiveObjectNode(FidgetTreeNode, Node):
    bl_idname = "FidgetActiveObjectNode"
    bl_label = "Active Object"

    def init(self, context):
        self.outputs.new("FidgetBoolSocket", "Object")

    def draw_buttons(self, context, layout):
        layout.separator()

class FidgetStatementNode(FidgetTreeNode, Node):
    bl_idname = "FidgetStatementNode"
    bl_label = "Statement"

    def init(self, context):
        self.outputs.new("FidgetBoolSocket", "")

    def draw_buttons(self, context, layout):
        layout.separator()

class FidgetOutputNode(FidgetTreeNode, Node):
    bl_idname = "FidgetOutputNode"
    bl_label = "Output"

    button = EnumProperty(
        name = "Fidget Button",
        description = "The fidget button to target",
        items = [
            ("LEFT", "Left Button", ""),
            ("RIGHT", "Right Button", ""),
            ("TOP", "Top Button", "")],
        default = "TOP")

    mode = EnumProperty(
        name = "Fidget Mode",
        description = "The fidget mode to target",
        items = [
            ("MODE3", "Mode 3", ""),
            ("MODE2", "Mode 2", ""),
            ("MODE1", "Mode 1", "")],
        default = "MODE1")

    def init(self, context):
        self.inputs.new("FidgetCommandSocket", "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "button", text="")
        layout.prop(self, "mode", text="")

        row = layout.row(align=True)
        row.scale_y = 1.25
        op = row.operator("fidget.update")
        op.output_id = str((self.id_data.name, self.name))
        op.write = True

        # TODO: write_file and reset behavior
        # row.operator("fidget.save", text="", icon="FILE_TICK")
        # row.operator("fidget.reset", text="", icon="LOAD_FACTORY")

class FidgetNodeCategory(NodeCategory):

    @classmethod
    def poll(build, context):
        return context.space_data.tree_type == "FidgetNodeTree"

node_categories = [
    FidgetNodeCategory("FIDGETINPUT", "Input", items=[
        NodeItem("FidgetCommandNode"),
        NodeItem("FidgetSwitchNode"),
        NodeItem("FidgetScriptNode")]),
    FidgetNodeCategory("FIDGETLOGIC", "Logic", items=[
        NodeItem("FidgetCompareNode"),
        NodeItem("FidgetObjectModeNode"),
        NodeItem("FidgetActiveObjectNode"),
        NodeItem("FidgetStatementNode")]),
    FidgetNodeCategory("FIDGETOUTPUT", "Output", items=[
        NodeItem("FidgetOutputNode")]),
    FidgetNodeCategory("LAYOUT", "Layout", items=[
        NodeItem("NodeFrame"),
        NodeItem("NodeReroute")])]

class FidgetUpdateOperator(FidgetNodeOperators, Operator):
    bl_idname = "fidget.update"
    bl_label = "Update"
    bl_description = "Update this fidget button"

    output_id = StringProperty()
    write = BoolProperty()
    reset = BoolProperty()

    @staticmethod
    def socket_type(socket):
        types = {
            'FidgetBoolSocket': 'bool',
            'FidgetCommandSocket': 'command'}

        return types[socket.bl_idname]

    @staticmethod
    def get_input(socket):
        return socket.links[0].from_node if socket.links else None

    def execute(self, context):
        try: tree_name, output_name = eval(self.output_id)
        except Exception as error:
            traceback.print_exc()
            tree_name, output_name = ('NodeTree', 'Output')

        tree = bpy.data.node_groups[tree_name]
        self.output = tree.nodes[output_name]

        links = self.output.inputs[0].links

        if len(links):
            self.input = links[0].from_node

            if self.input.bl_idname in {'FidgetCommandNode', 'FidgetScriptNode', 'FidgetSwitchNode'}:
                self.build(context)

                if self.error_message:
                    self.report({'WARNING'}, self.error_message)

                    return {'CANCELLED'}

            else:
                self.report({'WARNING'}, "{} node is an invalid input command for {}".format(self.input.bl_label.capitalize(), self.output.bl_label.lower()))

                return {'CANCELLED'}

        elif self.output.inputs[0].command:
            self.build(context)

            if self.error_message:
                self.report({'WARNING'}, self.error_message)

                return {'CANCELLED'}

        else:
            self.report({'WARNING'}, "Must have a command for output")

            return {'CANCELLED'}

        return {'FINISHED'}

    def build(self, context):
        self.error_message = ""
        self.command_value = "import bpy\n\ndef command(self, context, event):\n"
        self.indent = 1

        if hasattr(self, "input"):
            self.command_value += self.node_logic(self.input)

        else:
            self.command_value += self.socket_logic(self.output.inputs[0])

        if not self.error_message:
            self.set_output()

    def node_logic(self, node):
        return getattr(self, node.bl_idname[6:-4].lower())(node)

    def socket_logic(self, socket):
        node = self.get_input(socket)
        return self.node_logic(node) if node else self.no_input(socket)

    def no_input(self, socket):
        # TODO: handle boolean socket type
        return socket.command

    def set_output(self):
        self.command_value.expandtabs(tabsize=1)
        print("\n" + self.command_value + "\n")

        # if self.write:
        #     self.replace_command()
        # if self.reset:
        #     pass

    def replace_command(self):
        code = compile(self.command_value, "", "exec")

        new_command = {}

        exec(code, new_command)

        setattr(getattr(button, "{}_{}".format(self.output.button.lower(), self.output.mode.lower())), "command", new_command['command'])

    def command(self, node):
        return node.outputs[0].command

    def script(self, node):
        return ""

    def switch(self, node):
        return node.name

    def compare(self, node):
        logic = {
            'AND': lambda a, b: "{bool1} and {bool2}".format(bool1=a, bool2=b),
            'OR': lambda a, b: "{bool1} or {bool2}".format(bool1=a, bool2=b),
            'NAND': lambda a, b: "(not ({bool1} and {bool2}))".format(bool1=a, bool2=b),
            'NOR': lambda a, b: "(not ({bool1} or {bool2}))".format(bool1=a, bool2=b),
            'XOR': lambda a, b: "(({bool1} and not {bool2}) or (not {bool1} and {bool2}))".format(bool1=a, bool2=b),
            'XNOR': lambda a, b: "(not (({bool1} and not {bool2}) or (not {bool1} and {bool2})))".format(bool1=a, bool2=b)}

        bool1 = self.socket_logic(node.inputs[0])
        bool2 = self.socket_logic(node.inputs[1])

        return logic[node.outputs[0].logic](bool1, bool2)

    def objectmode(self, node):
        logic = {
            'OBJECT': "context.active_object.mode == 'OBJECT'",
            'EDIT': "context.active_object.mode == 'EDIT'",
            'SCULPT': "context.active_object.mode == 'SCULPT'",
            'VERTEX_PAINT': "context.active_object.mode == 'VERTEX_PAINT'",
            'WEIGHT_PAINT': "context.active_object.mode == 'WEIGHT_PAINT'",
            'TEXTURE_PAINT': "context.active_object.mode == 'TEXTURE_PAINT'",
            'PARTICLE_EDIT': "context.active_object.mode == 'PARTICLE_EDIT'"}

        return logic[node.outputs[0].mode]

    def activeobject(self, node):
        if node.outputs['Object'].value:
            return "context.active_object"
        else:
            return "(not context.active_object)"

    def statement(self, node):
        return node.outputs[0].statement

def nodes_register():
    nodeitems_utils.register_node_categories("FIDGET_NODES", node_categories)

def nodes_unregister():
    nodeitems_utils.unregister_node_categories("FIDGET_NODES")
