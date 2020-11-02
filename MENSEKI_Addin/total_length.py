#FusionAPI_python Addin
#Author-kantoku
#Description-selected total area

import adsk.core, adsk.fusion, traceback
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase

_selInfo = ['dlgSel','エッジの選択','-']
_txtInfo = ['dlgtxt','合計長さ','-']

_covunit = 0.0
_defLenUnit = ''

class total_length(Fusion360CommandBase):

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
        length = 0.0
        for idx in range(selIpt.selectionCount):
            length += selIpt.selection(idx).entity.length

        global _covunit, _defLenUnit
        length = length * _covunit
        length_txt = '{:.3e}　{}\n{}　{}'.format(length, _defLenUnit, length, _defLenUnit)

        selIpt.commandPrompt = '{0}　本合計\n'.format(selIpt.selectionCount) + length_txt

        # Text Input
        global _txtInfo
        txtIpt :adsk.core.TextBoxCommandInput = inputs.itemById(_txtInfo[0])
        txtIpt.text = length_txt

    def on_create(
        self,
        command: adsk.core.Command,
        inputs: adsk.core.CommandInputs):

        # unit
        global _defLenUnit, _covunit
        ao = AppObjects()
        unitsMgr = ao.units_manager
        _defLenUnit = unitsMgr.defaultLengthUnits
        tmp = unitsMgr.convert(1, unitsMgr.internalUnits, _defLenUnit)
        _covunit = tmp

        # command
        command.isOKButtonVisible = False

        global _selInfo
        selIpt :adsk.core.SelectionCommandInput = inputs.addSelectionInput(
            _selInfo[0], _selInfo[1], _selInfo[2])
        selIpt.setSelectionLimits(0)
        selIpt.addSelectionFilter('Edges')
        selIpt.commandPrompt = _selInfo[1]

        global _txtInfo
        inputs.addTextBoxCommandInput(
            _txtInfo[0], _txtInfo[1], _txtInfo[2], 2, True)