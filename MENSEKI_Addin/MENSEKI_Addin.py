#FusionAPI_python_Addin MENSEKI_Addin
#Author-kantoku
#Description-

#using Fusion360AddinSkeleton
#https://github.com/tapnair/Fusion360AddinSkeleton
#Special thanks:Patrick Rainsberry

import adsk.core
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .total_area import total_area
from .total_volume import total_volume

commands = []
command_definitions = []

# Set to True to display various useful messages when debugging your app
debug = False

def run(context):

    # 面積
    cmd = {
        'cmd_name': '面積',
        'cmd_description': '選択された面の合計面積',
        'cmd_id': 'total_area_id',
        'cmd_resources': './resources/total_area',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'InspectPanel',
        'class': total_area
    }
    command_definitions.append(cmd)

    # 体積
    cmd = {
        'cmd_name': '体積',
        'cmd_description': '選択されたボディの合計体積',
        'cmd_id': 'total_volume_id',
        'cmd_resources': './resources/total_volume',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'InspectPanel',
        'class': total_volume
    }
    command_definitions.append(cmd)

    # Don't change anything below here:
    for cmd_def in command_definitions:
        command = cmd_def['class'](cmd_def, debug)
        commands.append(command)

        for run_command in commands:
            run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()
