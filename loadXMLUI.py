#==============================================================================
# Namn:      Giedre Jursenaite                                 ================
# Datum:     2018-12-04                                        ================
#==============================================================================

# Imports:
from maya import OpenMayaUI as omui
import pymel.core as pm
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtWidgets 
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
import sys

# Load Window:
def getMayaWin():
	mayaWinPtr = omui.MQtUtil.mainWindow( )
	mayaWin = wrapInstance( long( mayaWinPtr ), QtWidgets.QMainWindow )

# Loads UI through path:
def loadUI( path ):
	loader = QUiLoader()
	uiFile = QFile( path )

	dirIconShapes = ""
	buff = None

	if uiFile.exists():
		dirIconShapes = path
		uiFile.open( QFile.ReadOnly )

		buff = QByteArray( uiFile.readAll() )
		uiFile.close()
	else:
		print "UI file missing! Exiting..."
		exit(-1)

	fixXML( path, buff )
	qbuff = QBuffer()
	qbuff.open( QBuffer.ReadOnly | QBuffer.WriteOnly )
	qbuff.write( buff )
	qbuff.seek( 0 )
	ui = loader.load( qbuff, parentWidget = getMayaWin() )
	ui.path = path

	return ui

# Cleans up path:
def fixXML( path, qbyteArray ):
	# first replace forward slashes for backslashes
	if path[-1] != '/':
		path += '/'
	path = path.replace( "/", "\\" )

	# construct whole new path with <pixmap> at the begining
	tempArr = QByteArray( "<pixmap>" + path + "\\" )

	# search for the word <pixmap>
	lastPos = qbyteArray.indexOf( "<pixmap>", 0 )
	while lastPos != -1:
		qbyteArray.replace( lastPos, len( "<pixmap>" ), tempArr )
		lastPos = qbyteArray.indexOf( "<pixmap>", lastPos + 1 )
	return

# Creates class for UI controllers:
class UIController:
	def __init__(self, ui):

		self.ui = ui
		ui.setWindowFlags(Qt.WindowStaysOnTopHint)

#==============================================================================
#//////////////////////////////////////////////////////////////////////////////
#==============================================================================
# Imports Import and Export Scripts:
sys.path.append("C:/Users/.../BlendAnimations/")

import BinaryExportForUI
reload(BinaryExportForUI)

import BinaryImportForUI
reload(BinaryImportForUI)

# Loads All UI for the Script:
ui = loadUI("C:/Users/.../BlendAnimations/UI/ChooseOneAlternative.ui")
importUI = loadUI("C:/Users/.../BlendAnimations/UI/ChooseAnimations.ui")
exportUI = loadUI("C:/Users/.../BlendAnimations/UI/ExportAnimations.ui")
jointUI = loadUI("C:/Users/.../BlendAnimations/UI/AjustJointsForLayers.ui")
bakeAnimUI = loadUI("C:/Users/.../BlendAnimations/UI/BakeAnimations.ui")

# Global lists
# Skleton
hirarchy = []
orientations = []
roatations = []

parentOrentations = []
parentOrentationsInvert = []

parentRotations = []
parentRotationsInvert = []

perentMatrixList = []
perentMatrixListInvers = []

# Binary file
jointNameListAnim1 = []
jointMatrixesListAnim1 = []
nrOFFramesAndJointsAnim1 = []

jointNameListAnim2 = []
jointMatrixesListAnim2 = []
nrOFFramesAndJointsAnim2 = []

jointNameListAnim3 = []
jointMatrixesListAnim3 = []
nrOFFramesAndJointsAnim3 = []

jointNameListAnim4 = []
jointMatrixesListAnim4 = []
nrOFFramesAndJointsAnim4 = []

pathsList1 = []
pathsList2 = []
pathsList3 = []
pathsList4 = []

animLayerList1 = []
animLayerList2 = []
animLayerList3 = []
animLayerList4 = []

# Creates class for Main Window.
uiCtrl1 = UIController(ui)
# Shows Main Window:
ui.show()

# Creates other classes:
# Choose animations to import Window:
uiCtrl2 = UIController(importUI)
# Export animation Window:
uiCtrl3 = UIController(exportUI)
# Ajust joints for import animations Window:
uiCtrl4 = UIController(jointUI)
# Ajust weights and bake animation Window:
uiCtrl5 = UIController(bakeAnimUI)

#==============================================================================

# The first Window on click events:
def OpenImport():
    # Hide Main UI window and show import animations UI window
    ui.hide()
    # Show import animations UI window
    importUI.show()
    
    
def OpenExport():
    
    if(len(hirarchy) > 0):
        del hirarchy[:]
        del orientations[:]
        del roatations[:]
        del parentOrentations[:]
        del parentOrentationsInvert[:]
        del parentRotations[:]
        del parentRotationsInvert[:]
        del perentMatrixList[:]
        del perentMatrixListInvers[:]
    
    BinaryExportForUI.HirarchyListCreator(hirarchy, orientations, roatations, perentMatrixList, perentMatrixListInvers, parentOrentations, parentOrentationsInvert, parentRotations, parentRotationsInvert)
    
    # Hide Main UI window and show import animations UI window
    ui.hide()
    # Show export animations UI window
    exportUI.show()
    
    for h in hirarchy:
        exportUI.SourceList.addItem(str(h))

#==============================================================================

def FindAnimPath1():
    path = BinaryImportForUI.OpenFiles()
    
    if(path == None):
        return
        
    nameString = str(path)
    nameString = nameString.split("'")
    nameString = nameString[1]
    if(importUI.AnimList1.count()>0):
        importUI.AnimList1.takeItem(0)
    importUI.AnimList1.addItem(str(nameString))
    if(len(pathsList1)>0):
        pathsList1.pop(0)
    pathsList1.append(path)

def FindAnimPath2():
    path = BinaryImportForUI.OpenFiles()
        
    if(path == None):
        return
     
    nameString = str(path)
    nameString = nameString.split("'")
    nameString = nameString[1]
    if(importUI.AnimList2.count()>0):
        importUI.AnimList2.takeItem(0)
    importUI.AnimList2.addItem(str(nameString))
    if(len(pathsList2)>0):
        pathsList2.pop(0)
    pathsList2.append(path)
        
def FindAnimPath3():
    path = BinaryImportForUI.OpenFiles()
        
    if(path == None):
        return
     
    nameString = str(path)
    nameString = nameString.split("'")
    nameString = nameString[1]
    if(importUI.AnimList3.count()>0):
        importUI.AnimList3.takeItem(0)
    importUI.AnimList3.addItem(str(nameString))
    if(len(pathsList3)>0):
        pathsList3.pop(0)
    pathsList3.append(path)
    
def FindAnimPath4():
    path = BinaryImportForUI.OpenFiles()
        
    if(path == None):
        return
     
    nameString = str(path)
    nameString = nameString.split("'")
    nameString = nameString[1]
    if(importUI.AnimList4.count()>0):
        importUI.AnimList4.takeItem(0)
    importUI.AnimList4.addItem(str(nameString))
    if(len(pathsList4)>0):
        pathsList4.pop(0)
    pathsList4.append(path)
        
def LoadAnimations():
    if(len(pathsList1)>0):
        BinaryImportForUI.ReadFromFiles(pathsList1[0], jointNameListAnim1, jointMatrixesListAnim1, nrOFFramesAndJointsAnim1)
    if(len(pathsList2)>0):
        BinaryImportForUI.ReadFromFiles(pathsList2[0], jointNameListAnim2, jointMatrixesListAnim2, nrOFFramesAndJointsAnim2)
    if(len(pathsList3)>0):
        BinaryImportForUI.ReadFromFiles(pathsList3[0], jointNameListAnim3, jointMatrixesListAnim3, nrOFFramesAndJointsAnim3)
    if(len(pathsList4)>0):
        BinaryImportForUI.ReadFromFiles(pathsList4[0], jointNameListAnim4, jointMatrixesListAnim4, nrOFFramesAndJointsAnim4)

    BinaryImportForUI.HirarchyListCreator(hirarchy, orientations, roatations, perentMatrixList, perentMatrixListInvers, parentOrentations, parentOrentationsInvert, parentRotations, perentMatrixListInvers)

    importUI.hide()
    jointUI.show()
    
    for h in hirarchy:
        jointUI.TargetList.addItem(str(h))
        
    if(len(jointNameListAnim1)>0):
        for l1 in jointNameListAnim1:
            jointUI.AnimList1.addItem(l1)
    if(len(jointNameListAnim2)>0):
        for l2 in jointNameListAnim2:
            jointUI.AnimList2.addItem(l2)
    if(len(jointNameListAnim3)>0):
        for l3 in jointNameListAnim3:
            jointUI.AnimList3.addItem(l3)
    if(len(jointNameListAnim4)>0):
        for l4 in jointNameListAnim4:
            jointUI.AnimList4.addItem(l4)
    
#==============================================================================

def TargetUp():
    currentRow = jointUI.TargetList.currentRow()
    
    temp = hirarchy[currentRow]
    hirarchy[currentRow] = hirarchy[currentRow - 1]
    hirarchy[currentRow - 1] = temp
    
    currentItem = jointUI.TargetList.takeItem(currentRow)
    jointUI.TargetList.insertItem(currentRow - 1, currentItem)
    jointUI.TargetList.setCurrentRow(currentRow - 1)
    
    temp = parentOrentations[currentRow]
    parentOrentations[currentRow] = parentOrentations[currentRow - 1]
    parentOrentations[currentRow - 1] = temp
    
    temp = parentOrentationsInvert[currentRow]
    parentOrentationsInvert[currentRow] = parentOrentationsInvert[currentRow - 1]
    parentOrentationsInvert[currentRow - 1] = temp
    
    temp = parentRotations[currentRow]
    parentRotations[currentRow] = parentRotations[currentRow - 1]
    parentRotations[currentRow - 1] = temp
    
    temp = perentMatrixList[currentRow]
    perentMatrixList[currentRow] = perentMatrixList[currentRow - 1]
    perentMatrixList[currentRow - 1] = temp
    
    temp = perentMatrixListInvers[currentRow]
    perentMatrixListInvers[currentRow] = perentMatrixListInvers[currentRow - 1]
    perentMatrixListInvers[currentRow - 1] = temp
    
def TargetDown():
    currentRow = jointUI.TargetList.currentRow()
    
    temp = hirarchy[currentRow]
    hirarchy[currentRow] = hirarchy[currentRow + 1]
    hirarchy[currentRow + 1] = temp
    
    currentItem = jointUI.TargetList.takeItem(currentRow)
    jointUI.TargetList.insertItem(currentRow + 1, currentItem)
    jointUI.TargetList.setCurrentRow(currentRow + 1)
    
    temp = parentOrentations[currentRow]
    parentOrentations[currentRow] = parentOrentations[currentRow + 1]
    parentOrentations[currentRow + 1] = temp
    
    temp = parentOrentationsInvert[currentRow]
    parentOrentationsInvert[currentRow] = parentOrentationsInvert[currentRow + 1]
    parentOrentationsInvert[currentRow + 1] = temp
    
    temp = parentRotations[currentRow]
    parentRotations[currentRow] = parentRotations[currentRow + 1]
    parentRotations[currentRow + 1] = temp
    
    temp = perentMatrixList[currentRow]
    perentMatrixList[currentRow] = perentMatrixList[currentRow + 1]
    perentMatrixList[currentRow + 1] = temp
    
    temp = perentMatrixListInvers[currentRow]
    perentMatrixListInvers[currentRow] = perentMatrixListInvers[currentRow + 1]
    perentMatrixListInvers[currentRow + 1] = temp
    
def TargetDelete():
    currentRow = jointUI.TargetList.currentRow()
    currentItem = jointUI.TargetList.takeItem(currentRow)
    
    hirarchy.pop(currentRow)
    
    parentOrentations.pop(currentRow)
    parentOrentationsInvert.pop(currentRow)
    
    parentRotations.pop(currentRow)
    
    perentMatrixList.pop(currentRow)
    perentMatrixListInvers.pop(currentRow)

def Anim1Up():
    currentRow = jointUI.AnimList1.currentRow()
    
    temp = jointNameListAnim1[currentRow]
    jointNameListAnim1[currentRow] = jointNameListAnim1[currentRow - 1]
    jointNameListAnim1[currentRow - 1] = temp
    
    currentItem = jointUI.AnimList1.takeItem(currentRow)
    jointUI.AnimList1.insertItem(currentRow - 1, currentItem)
    jointUI.AnimList1.setCurrentRow(currentRow - 1)
    
    temp = jointMatrixesListAnim1[currentRow]
    jointMatrixesListAnim1[currentRow] = jointMatrixesListAnim1[currentRow - 1]
    jointMatrixesListAnim1[currentRow - 1] = temp

def Anim2Up():
    currentRow = jointUI.AnimList2.currentRow()
    
    temp = jointNameListAnim2[currentRow]
    jointNameListAnim2[currentRow] = jointNameListAnim2[currentRow - 1]
    jointNameListAnim2[currentRow - 1] = temp
    
    currentItem = jointUI.AnimList2.takeItem(currentRow)
    jointUI.AnimList2.insertItem(currentRow - 1, currentItem)
    jointUI.AnimList2.setCurrentRow(currentRow - 1)
    
    temp = jointMatrixesListAnim2[currentRow]
    jointMatrixesListAnim2[currentRow] = jointMatrixesListAnim2[currentRow - 1]
    jointMatrixesListAnim2[currentRow - 1] = temp

def Anim3Up():
    currentRow = jointUI.AnimList3.currentRow()
    
    temp = jointNameListAnim3[currentRow]
    jointNameListAnim3[currentRow] = jointNameListAnim3[currentRow - 1]
    jointNameListAnim3[currentRow - 1] = temp
    
    currentItem = jointUI.AnimList3.takeItem(currentRow)
    jointUI.AnimList3.insertItem(currentRow - 1, currentItem)
    jointUI.AnimList3.setCurrentRow(currentRow - 1)
    
    temp = jointMatrixesListAnim3[currentRow]
    jointMatrixesListAnim3[currentRow] = jointMatrixesListAnim3[currentRow - 1]
    jointMatrixesListAnim3[currentRow - 1] = temp

def Anim4Up():
    currentRow = jointUI.AnimList4.currentRow()
    
    temp = jointNameListAnim4[currentRow]
    jointNameListAnim4[currentRow] = jointNameListAnim4[currentRow - 1]
    jointNameListAnim4[currentRow - 1] = temp
    
    currentItem = jointUI.AnimList4.takeItem(currentRow)
    jointUI.AnimList4.insertItem(currentRow - 1, currentItem)
    jointUI.AnimList4.setCurrentRow(currentRow - 1)
    
    temp = jointMatrixesListAnim4[currentRow]
    jointMatrixesListAnim4[currentRow] = jointMatrixesListAnim4[currentRow - 1]
    jointMatrixesListAnim4[currentRow - 1] = temp

def Anim1Down():
    currentRow = jointUI.AnimList1.currentRow()
    
    temp = jointNameListAnim1[currentRow]
    jointNameListAnim1[currentRow] = jointNameListAnim1[currentRow + 1]
    jointNameListAnim1[currentRow + 1] = temp
    
    currentItem = jointUI.AnimList1.takeItem(currentRow)
    jointUI.AnimList1.insertItem(currentRow + 1, currentItem)
    jointUI.AnimList1.setCurrentRow(currentRow + 1)
    
    temp = jointMatrixesListAnim1[currentRow]
    jointMatrixesListAnim1[currentRow] = jointMatrixesListAnim1[currentRow + 1]
    jointMatrixesListAnim1[currentRow + 1] = temp
    
def Anim2Down():
    currentRow = jointUI.AnimList2.currentRow()
    
    temp = jointNameListAnim2[currentRow]
    jointNameListAnim2[currentRow] = jointNameListAnim2[currentRow + 1]
    jointNameListAnim2[currentRow + 1] = temp
    
    currentItem = jointUI.AnimList2.takeItem(currentRow)
    jointUI.AnimList2.insertItem(currentRow + 1, currentItem)
    jointUI.AnimList2.setCurrentRow(currentRow + 1)
    
    temp = jointMatrixesListAnim2[currentRow]
    jointMatrixesListAnim2[currentRow] = jointMatrixesListAnim2[currentRow + 1]
    jointMatrixesListAnim2[currentRow + 1] = temp
    
def Anim3Down():
    currentRow = jointUI.AnimList3.currentRow()
    
    temp = jointNameListAnim3[currentRow]
    jointNameListAnim3[currentRow] = jointNameListAnim3[currentRow + 1]
    jointNameListAnim3[currentRow + 1] = temp
    
    currentItem = jointUI.AnimList3.takeItem(currentRow)
    jointUI.AnimList3.insertItem(currentRow + 1, currentItem)
    jointUI.AnimList3.setCurrentRow(currentRow + 1)
    
    temp = jointMatrixesListAnim3[currentRow]
    jointMatrixesListAnim3[currentRow] = jointMatrixesListAnim3[currentRow + 1]
    jointMatrixesListAnim3[currentRow + 1] = temp
    
def Anim4Down():
    currentRow = jointUI.AnimList4.currentRow()
    
    temp = jointNameListAnim4[currentRow]
    jointNameListAnim4[currentRow] = jointNameListAnim4[currentRow + 1]
    jointNameListAnim4[currentRow + 1] = temp
    
    currentItem = jointUI.AnimList4.takeItem(currentRow)
    jointUI.AnimList4.insertItem(currentRow + 1, currentItem)
    jointUI.AnimList4.setCurrentRow(currentRow + 1)
    
    temp = jointMatrixesListAnim4[currentRow]
    jointMatrixesListAnim4[currentRow] = jointMatrixesListAnim4[currentRow + 1]
    jointMatrixesListAnim4[currentRow + 1] = temp

def Anim1Delete():
    currentRow = jointUI.AnimList1.currentRow()
    currentItem = jointUI.AnimList1.takeItem(currentRow)
    
    jointNameListAnim1.pop(currentRow)
    
    jointMatrixesListAnim1.pop(currentRow)
        
def Anim2Delete():
    currentRow = jointUI.AnimList2.currentRow()
    currentItem = jointUI.AnimList2.takeItem(currentRow)
    
    jointNameListAnim2.pop(currentRow)
    
    jointMatrixesListAnim2.pop(currentRow)
        
def Anim3Delete():
    currentRow = jointUI.AnimList3.currentRow()
    currentItem = jointUI.AnimList3.takeItem(currentRow)
    
    jointNameListAnim3.pop(currentRow)
    
    jointMatrixesListAnim3.pop(currentRow)
        
def Anim4Delete():
    currentRow = jointUI.AnimList4.currentRow()
    currentItem = jointUI.AnimList4.takeItem(currentRow)
    
    jointNameListAnim4.pop(currentRow)
    
    jointMatrixesListAnim4.pop(currentRow)
          
def CreateBakedLayers():
    
    nope1 = 1
    nope2 = 1
    nope3 = 1
    nope4 = 1
    
    if(len(jointMatrixesListAnim1) > 0):
        if(len(hirarchy) == len(jointNameListAnim1)):
            animName = BinaryImportForUI.FindAnimName(pathsList1[0])
            pathsList1.append(animName)
            BinaryImportForUI.CreateLayers(animName, hirarchy, nrOFFramesAndJointsAnim1[0], parentRotations, parentOrentations, parentOrentationsInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesListAnim1, animLayerList1)
        else:
            sys.stdout.write('Error: The number of selected joints for target skeletton and source animation 1 must be the same.')
            nope1 = 0
    
    if(len(jointMatrixesListAnim2) > 0):    
        if(len(hirarchy) == len(jointNameListAnim2)):
            animName = BinaryImportForUI.FindAnimName(pathsList2[0])
            pathsList2.append(animName)
            BinaryImportForUI.CreateLayers(animName, hirarchy, nrOFFramesAndJointsAnim2[0], parentRotations, parentOrentations, parentOrentationsInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesListAnim2, animLayerList2)
        else:
            sys.stdout.write('Error: The number of selected joints for target skeletton and source animation 2 must be the same.')
            nope2 = 0
    
    if(len(jointMatrixesListAnim3) > 0):    
        if(len(hirarchy) == len(jointNameListAnim3)):
            animName = BinaryImportForUI.FindAnimName(pathsList3[0])
            pathsList3.append(animName)
            BinaryImportForUI.CreateLayers(animName, hirarchy, nrOFFramesAndJointsAnim3[0], parentRotations, parentOrentations, parentOrentationsInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesListAnim3, animLayerList3)
        else:
            sys.stdout.write('Error: The number of selected joints for target skeletton and source animation 3 must be the same.')
            nope3 = 0
    
    if(len(jointMatrixesListAnim4) > 0):    
        if(len(hirarchy) == len(jointNameListAnim4)):
            animName = BinaryImportForUI.FindAnimName(pathsList4[0])
            pathsList4.append(animName)
            BinaryImportForUI.CreateLayers(animName, hirarchy, nrOFFramesAndJointsAnim4[0], parentRotations, parentOrentations, parentOrentationsInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesListAnim4, animLayerList4)
        else:
            sys.stdout.write('Error: The number of selected joints for target skeletton and source animation 4 must be the same.')
            nope4 = 0
    
    if nope1 is not 0 and nope2 is not 0 and nope3 is not 0 and nope4 is not 0:
        jointUI.hide()
        bakeAnimUI.show()
        pm.play(f = True)
        
        if(len(pathsList1) > 0):
            bakeAnimUI.AnimNameRef1.addItem(pathsList1[1])
            
        if(len(pathsList2) > 0):
            bakeAnimUI.AnimNameRef2.addItem(pathsList2[1])
            
        if(len(pathsList3) > 0):
            bakeAnimUI.AnimNameRef3.addItem(pathsList3[1])
            
        if(len(pathsList4) > 0):
            bakeAnimUI.AnimNameRef4.addItem(pathsList4[1])
            
def Slider1Moved():
    newValue = bakeAnimUI.WeightSlider1.value()
    newValue = float(newValue)/100.0
    pm.animLayer(pathsList1[1], edit = True, w=newValue)
    
def Slider2Moved():
    newValue = bakeAnimUI.WeightSlider2.value()
    newValue = float(newValue)/100.0
    pm.animLayer(pathsList2[1], edit = True, w=newValue)
    
def Slider3Moved():
    newValue = bakeAnimUI.WeightSlider3.value()
    newValue = float(newValue)/100.0
    pm.animLayer(pathsList3[1], edit = True, w=newValue)
    
def Slider4Moved():
    newValue = bakeAnimUI.WeightSlider4.value()
    newValue = float(newValue)/100.0
    pm.animLayer(pathsList4[1], edit = True, w=newValue)
    
#==============================================================================

def BakeAnimationsToBaseLayer():
    pm.play(st = False)
    BinaryImportForUI.BakeAnimations(hirarchy)
    
    if(len(animLayerList1) > 0):
        pm.delete(animLayerList1[0])
    if(len(animLayerList2) > 0):
        pm.delete(animLayerList2[0])
    if(len(animLayerList3) > 0):
        pm.delete(animLayerList3[0])
    if(len(animLayerList4) > 0):
        pm.delete(animLayerList4[0])
    
    bakeAnimUI.hide()
    ui.show()
    
#==============================================================================

def SourceUp():
    currentRow = exportUI.SourceList.currentRow()
    
    temp = hirarchy[currentRow]
    hirarchy[currentRow] = hirarchy[currentRow - 1]
    hirarchy[currentRow - 1] = temp
    
    currentItem = exportUI.SourceList.takeItem(currentRow)
    exportUI.SourceList.insertItem(currentRow - 1, currentItem)
    exportUI.SourceList.setCurrentRow(currentRow - 1)
    
    temp = parentOrentations[currentRow]
    parentOrentations[currentRow] = parentOrentations[currentRow - 1]
    parentOrentations[currentRow - 1] = temp
    
    temp = parentOrentationsInvert[currentRow]
    parentOrentationsInvert[currentRow] = parentOrentationsInvert[currentRow - 1]
    parentOrentationsInvert[currentRow - 1] = temp
    
    temp = parentRotations[currentRow]
    parentRotations[currentRow] = parentRotations[currentRow - 1]
    parentRotations[currentRow - 1] = temp
    
    temp = parentRotationsInvert[currentRow]
    parentRotationsInvert[currentRow] = parentRotationsInvert[currentRow - 1]
    parentRotationsInvert[currentRow - 1] = temp
    
    temp = perentMatrixList[currentRow]
    perentMatrixList[currentRow] = perentMatrixList[currentRow - 1]
    perentMatrixList[currentRow - 1] = temp
    
    temp = perentMatrixListInvers[currentRow]
    perentMatrixListInvers[currentRow] = perentMatrixListInvers[currentRow - 1]
    perentMatrixListInvers[currentRow - 1] = temp
       
def SourceDown():
    currentRow = exportUI.SourceList.currentRow()
    
    temp = hirarchy[currentRow]
    hirarchy[currentRow] = hirarchy[currentRow + 1]
    hirarchy[currentRow + 1] = temp
    
    currentItem = exportUI.SourceList.takeItem(currentRow)
    exportUI.SourceList.insertItem(currentRow + 1, currentItem)
    exportUI.SourceList.setCurrentRow(currentRow + 1)
    
    temp = parentOrentations[currentRow]
    parentOrentations[currentRow] = parentOrentations[currentRow + 1]
    parentOrentations[currentRow + 1] = temp
    
    temp = parentOrentationsInvert[currentRow]
    parentOrentationsInvert[currentRow] = parentOrentationsInvert[currentRow + 1]
    parentOrentationsInvert[currentRow + 1] = temp
    
    temp = parentRotations[currentRow]
    parentRotations[currentRow] = parentRotations[currentRow + 1]
    parentRotations[currentRow + 1] = temp
    
    temp = parentRotationsInvert[currentRow]
    parentRotationsInvert[currentRow] = parentRotationsInvert[currentRow + 1]
    parentRotationsInvert[currentRow + 1] = temp
    
    temp = perentMatrixList[currentRow]
    perentMatrixList[currentRow] = perentMatrixList[currentRow + 1]
    perentMatrixList[currentRow + 1] = temp
    
    temp = perentMatrixListInvers[currentRow]
    perentMatrixListInvers[currentRow] = perentMatrixListInvers[currentRow + 1]
    perentMatrixListInvers[currentRow + 1] = temp
    
def SourceDelete():
    currentRow = exportUI.SourceList.currentRow()
    currentItem = exportUI.SourceList.takeItem(currentRow)
    
    hirarchy.pop(currentRow)
    
    parentOrentations.pop(currentRow)
    parentOrentationsInvert.pop(currentRow)
    
    parentRotations.pop(currentRow)
    parentRotationsInvert.pop(currentRow)
    
    perentMatrixList.pop(currentRow)
    perentMatrixListInvers.pop(currentRow)
   
def ExportAnimations():
    filePath = BinaryExportForUI.CreateFilePath()
        
    if(filePath == None):
        return
    
    frameStart = exportUI.FramesFromSpin.value()
    frameEnd = exportUI.FramesToSpin.value()
    
    nrOfframes = frameEnd - frameStart
    
    if(frameEnd is not frameStart):
        BinaryExportForUI.WriteToFile(filePath, hirarchy, parentRotationsInvert, parentOrentationsInvert, perentMatrixListInvers, perentMatrixList, parentOrentations, frameStart, frameEnd, nrOfframes) 
        exportUI.hide()
        
        ui.destroy()
        importUI.destroy()
        jointUI.destroy()
        bakeAnimUI.destroy()
        exportUI.destroy()
        #sys.exit()
        
    else:
        sys.stdout.write('Error: The number of frames should be more than 0.')
#==============================================================================
# Main UI window buttons:
ui.ImportAnim.clicked.connect(OpenImport)
ui.ExportAnim.clicked.connect(OpenExport)

importUI.ChoseAnim1.clicked.connect(FindAnimPath1)
importUI.ChoseAnim2.clicked.connect(FindAnimPath2)
importUI.ChoseAnim3.clicked.connect(FindAnimPath3)
importUI.ChoseAnim4.clicked.connect(FindAnimPath4)
importUI.LoadAnimButton.clicked.connect(LoadAnimations)

jointUI.CreateLayersButton.clicked.connect(CreateBakedLayers)
jointUI.TargetUp.clicked.connect(TargetUp)
jointUI.TargetDelete.clicked.connect(TargetDelete)
jointUI.TargetDown.clicked.connect(TargetDown)
jointUI.Anim1Up.clicked.connect(Anim1Up)
jointUI.Anim2Up.clicked.connect(Anim2Up)
jointUI.Anim3Up.clicked.connect(Anim3Up)
jointUI.Anim4Up.clicked.connect(Anim4Up)
jointUI.Anim1Delete.clicked.connect(Anim1Delete)
jointUI.Anim2Delete.clicked.connect(Anim2Delete)
jointUI.Anim3Delete.clicked.connect(Anim3Delete)
jointUI.Anim4Delete.clicked.connect(Anim4Delete)
jointUI.Anim1Down.clicked.connect(Anim1Down)
jointUI.Anim2Down.clicked.connect(Anim2Down)
jointUI.Anim3Down.clicked.connect(Anim3Down)
jointUI.Anim4Down.clicked.connect(Anim4Down)

bakeAnimUI.BakeAnimButton.clicked.connect(BakeAnimationsToBaseLayer)

bakeAnimUI.WeightSlider1.sliderMoved.connect(Slider1Moved)
bakeAnimUI.WeightSlider2.sliderMoved.connect(Slider2Moved)
bakeAnimUI.WeightSlider3.sliderMoved.connect(Slider3Moved)
bakeAnimUI.WeightSlider4.sliderMoved.connect(Slider4Moved)

exportUI.SourceUp.clicked.connect(SourceUp)
exportUI.SourceDelete.clicked.connect(SourceDelete)
exportUI.SourceDown.clicked.connect(SourceDown)
exportUI.ExportAnimationButton.clicked.connect(ExportAnimations)
