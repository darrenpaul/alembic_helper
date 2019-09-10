#!/usr/bin/env python
import maya.cmds as cmds
import os


BASE_ATTRIBUTES = [
    "-frameRange",
    "-dataFormat\n ogawa"
]


class Helper:
    def __init__(self, node=None, output=None):
        self.check_alembic_plugin()
        self._node = node
        self._output = output
        self._command = self.__create_default_command()

    def set_alembic_node(self, node):
        self._node = node

    @property
    def get_alembic_node(self):
        return self._node

    def set_alembic_output(self, output):
        self._output = output

    @property
    def get_alembic_output(self):
        return self._output

    def set_alembic_command(self, commands):
        self._command = self.__create_default_command(
            extra_attributes=commands)

    @property
    def get_alembic_command(self):
        return self._command

    def export_alembic(self):
        ["-root {}".format(str(self._node)), "-file {}".format(self._output)]
        if os.path.exists(os.path.dirname(self._output)):
            cmds.AbcExport(j=self._command)

    def __create_default_command(self, extra_attributes=None):
        attrs = BASE_ATTRIBUTES
        if extra_attributes is not None:
            attrs = attrs + extra_attributes
        attrs = attrs + self.__get_write_attributes()
        return " ".join(attrs)

    def __get_write_attributes(self):
        return ["-root {}".format(self._node), "-file {}".format(self._output)]

    @classmethod
    def check_alembic_plugin(cls):
        if cmds.pluginInfo('AbcExport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcExport.so")
        if cmds.pluginInfo('AbcImport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcImport.so")
