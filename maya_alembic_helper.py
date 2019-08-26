import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0])))).replace(os.sep, "/"))
from pc_utilities import pc_helper
from maya.cmds import cmds


class PCAlembic:
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

        self.command = self.__create_default_command()

    @classmethod
    def check_alembic_plugin(cls):
        if cmds.pluginInfo('AbcExport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcExport.so")
        if cmds.pluginInfo('AbcImport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcImport.so")
