#FusionAPI_python Addin
#Author-kantoku
#Description-selected total volume

import adsk.core, adsk.fusion, traceback
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase

_selInfo = ['dlgSel','ボディの選択','-']
_txtVolInfo = ['dlgtxt','合計体積','-']
_txtCogInfo = ['dlgCogtxt','重心','-']

_covunitVol = 0.0
_covunitLng = 0.0
_defLenUnit = ''

class total_volume(Fusion360CommandBase):

    def on_input_changed(
        self,
        command: adsk.core.Command,
        inputs: adsk.core.CommandInputs,
        changed_input,
        input_values):

        global _selInfo
        if changed_input.id != _selInfo[0]:
            return

        # Select Input
        selIpt = changed_input
        volume = 0.0
        for idx in range(selIpt.selectionCount):
            volume += selIpt.selection(idx).entity.physicalProperties.volume

        global _covunitVol, _defLenUnit
        volume = volume * _covunitVol
        volume_txt = '{:.3e}　{}^3\n{}　{}^3'.format(volume, _defLenUnit, volume, _defLenUnit)

        selIpt.commandPrompt = '{0}　個合計\n'.format(selIpt.selectionCount) + volume_txt

        if selIpt.selectionCount == 1:
            cog = selIpt.selection(0).entity.physicalProperties.centerOfMass
            cogX = cog.x * _covunitLng
            cogY = cog.y * _covunitLng
            cogZ = cog.z * _covunitLng
            cog_txt = 'X{:.3e} {} Y{:.3e} {} Z{:.3e} {} \nX{} {} Y{} {} Z{} {}'.format(
                cogX, _defLenUnit, cogY, _defLenUnit, cogZ, _defLenUnit,
                cogX, _defLenUnit, cogY, _defLenUnit, cogZ, _defLenUnit)
        else:
            cog_txt = '-'

        # Text Input
        global _txtVolInfo
        txtVolIpt :adsk.core.TextBoxCommandInput = inputs.itemById(_txtVolInfo[0])
        txtVolIpt.text = volume_txt

        global _txtCogInfo
        txtCogIpt :adsk.core.TextBoxCommandInput = inputs.itemById(_txtCogInfo[0])
        txtCogIpt.text = cog_txt

    def on_create(
        self,
        command: adsk.core.Command,
        inputs: adsk.core.CommandInputs):

        # unit
        global _defLenUnit, _covunitVol, _covunitLng
        ao = AppObjects()
        unitsMgr = ao.units_manager
        _defLenUnit = unitsMgr.defaultLengthUnits
        tmp = unitsMgr.convert(1, unitsMgr.internalUnits, _defLenUnit)
        _covunitVol = tmp * tmp * tmp
        _covunitLng = tmp

        # command
        command.isOKButtonVisible = False

        global _selInfo
        selIpt :adsk.core.SelectionCommandInput = inputs.addSelectionInput(
            _selInfo[0], _selInfo[1], _selInfo[2])
        selIpt.setSelectionLimits(0)
        selIpt.addSelectionFilter('Bodies')
        selIpt.commandPrompt = _selInfo[1]

        global _txtVolInfo
        inputs.addTextBoxCommandInput(
            _txtVolInfo[0], _txtVolInfo[1], _txtVolInfo[2], 2, True)

        global _txtCogInfo
        inputs.addTextBoxCommandInput(
            _txtCogInfo[0], _txtCogInfo[1], _txtCogInfo[2], 6, True)