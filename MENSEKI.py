#FusionAPI_python
#Author-kantoku
#Description-選択面の合計面積を表示

import adsk.core, adsk.fusion, traceback

_app = None
_ui  = None
_handlers = []
_covunit = 0.0
_defLenUnit = ''

#選択面変更
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.firingEvent.sender
            inputs = cmd.commandInputs
            
            area = 0.0
            for sel in _ui.activeSelections:
                area = area + sel.entity.area
            
            global _covunit, _defLenUnit
            area = area * _covunit
            area_txt = '{:.3e}　{}^2\n{}　{}^2'.format(area, _defLenUnit, area, _defLenUnit)
            
            ta = inputs.itemById('total_area')
            ta.text = area_txt
            
            sl = inputs.itemById('selection')
            sl.commandPrompt = '{0}　枚合計\n'.format(_ui.activeSelections.count) + area_txt
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

#このコマンドのイベント・ダイアログ作成
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            #global _inputs, _handlers
            global _handlers
            cmd = adsk.core.Command.cast(args.command)
            inputs = cmd.commandInputs
            
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)    
            
            selectionInput = inputs.addSelectionInput('selection', '選択面', 'select　face')
            selectionInput.setSelectionLimits(0)
            selectionInput.addSelectionFilter('Faces')
            selectionInput.commandPrompt = 'Select Face'
            
            inputs.addTextBoxCommandInput('total_area', '合計面積', '-', 2, True)
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
#このコマンドの破棄
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            adsk.terminate()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    try:
        global _app, _ui, _covunit, _defLenUnit
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        
        des = _app.activeProduct
        unitsMgr = des.unitsManager
        _defLenUnit = unitsMgr.defaultLengthUnits
        tmp = unitsMgr.convert(1, unitsMgr.internalUnits, _defLenUnit)
        _covunit = tmp * tmp
        
        cmdDef = _ui.commandDefinitions.itemById('MENSEKI')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition('MENSEKI', '選択面の合計面積', 'total_area')

        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
        
        cmdDef.execute()

        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
