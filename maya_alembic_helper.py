from maya.cmds import cmds
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0])))).replace(os.sep, "/"))
from pc_utilities import pc_helper


BASE_ATTRIBUTES = [
    "-frameRange",
    "-dataFormat ogawa"
]


class MayaAlembic:
    def __init__(self, node, target_path):
        self.check_alembic_plugin()
        self.node = node
        self.output = pc_helper.set_file_extension(target_path, "abc")
        self.start_frame = cmds.playbackOptions(
            animationStartTime=True, query=True, edit=True)
        self.end_framme = cmds.playbackOptions(
            animationEndTime=True, query=True, edit=True)
        self.isolate = True
        self.bake = True
        self.custom_attributes = []
        self.command = self.__create_default_command()

    def export_alembic(self):
        ["-root {}".format(str(self.node)),"-file {}".format(self.exportPath)]
        if os.path.exists(os.path.dirname(self.output)):
            cmds.AbcExport(j=self.command)

    def __create_default_command(self, extra_attributes=None):
        attrs = BASE_ATTRIBUTES
        if self.custom_attributes:
            attrs = attrs + self.custom_attributes
        if extra_attributes is not None:
            attrs = attrs + extra_attributes
        attrs = attrs + self.__get_write_attributes()
        return " ".join(attrs)
    
    def __get_write_attributes(self):
        return ["-root {}".format(self.node),"-file {}".format(self.output)]

    @classmethod
    def check_alembic_plugin(cls):
        if cmds.pluginInfo('AbcExport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcExport.so")
        if cmds.pluginInfo('AbcImport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcImport.so")
