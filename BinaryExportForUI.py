# Imports:    
import pymel.core as pm
import pymel.core.datatypes as dt
import sys
import struct

# Get corect Hirarchy:   
def Hirarchy(node, hirarchy):
    
    for child in node.getChildren():

        hirarchy.append(child)
        
        if child.numChildren()>0:
            Hirarchy(child, hirarchy)

# Get root in Hierchy:
def ReversedHierarchy(node):
    if node.getParent():
        tempPerent = node.getParent()
        newTempPerent = tempPerent
    
        if tempPerent.getParent():
            ReversedHierarchy(tempPerent)
        else:
            newTempPerent = pm.select(newTempPerent)
            return newTempPerent
    else:
        node = pm.select(node)
        return node

# Get Oreantations and Rotations for Sorce:
def PerentRotAndOr(node, orient, jointsRoatations):
    if node.getParent():
        tempPerent = node.getParent()
        orient.append(tempPerent.getOrientation().asMatrix())
        
        rotation = dt.Matrix()
        pm.currentTime(0.0)
        rot = tempPerent.getRotation()
        rotation = dt.EulerRotation(rot).asMatrix() 
        jointsRoatations.append(rotation)
        
        if tempPerent.getParent():
            PerentRotAndOr(tempPerent, orient, jointsRoatations)

# Calculate perent matrix:
def CalculateOriAndRot(orientation, rJoints):
    calc = dt.Matrix()
    for o, j in zip(orientation, rJoints):
        calc *= o * j
    return calc

# Hierarchy Calculations:
def Orientations(hirarchy, orent, orentInvert):
    for s in hirarchy:
        orent.append(s.getOrientation().asMatrix())
        orentInvert.append(s.getOrientation().asMatrix().inverse())

# Create a path and name to file that is exported
def CreateFilePath():
    newFile = pm.fileDialog2(fm = 0, ds = 2, ff = '*.sb')
    if(newFile == None):
        sys.stdout.write('Warning: A name or a path for the file should be chosen.')
        return
    return newFile

# Create binary animation file
def WriteToFile(newFile, hirarchy, rotationsInvert, orentInvert, perentMatrixListInvers, perentMatrixList, orent, frameStart, frameEnd, nrOfframes):
    
    if(newFile[0] == None):
        sys.stdout.write('Error: A name or a path for the file was never chosen.')
        return
    
    exportFile = open(newFile[0], 'wb')
    
    exportFile.write(struct.pack('ii', nrOfframes, len(hirarchy)))
    
    frameList = list(range(frameStart, (frameEnd + 1)))
    
    for index, h in enumerate(hirarchy):
        exportFile.write(struct.pack('i', len(str(h))))
        exportFile.write(str(h))
        
        for i in frameList:
            
            fRotation = dt.Matrix()
            
            # Get Final source rotation at this keyframe:
            pm.currentTime(i)
    
            fRotation = h.getRotation()
            fRotation = dt.EulerRotation(fRotation).asMatrix()
            
            # Isolated rotation:
            k = rotationsInvert[index] * fRotation
            
            # World space rotation:
            kPrim = orentInvert[index] * perentMatrixListInvers[index] * k * perentMatrixList[index] * orent[index]
            
            
            # Export every float in matrix in one chunk of data:
            exportFile.write(struct.pack('ffffffffffffffff', kPrim.a00, kPrim.a01, kPrim.a02, kPrim.a03, kPrim.a10, kPrim.a11, kPrim.a12, kPrim.a13, kPrim.a20, kPrim.a21, kPrim.a22, kPrim.a23, kPrim.a30, kPrim.a31, kPrim.a32, kPrim.a33))
            
    exportFile.close()
    sys.stdout.write('Info: File successfully exported.')

      
# ========================================================
def HirarchyListCreator(hirarchy, orient, jointsRoatations, perentMatrixList, perentMatrixListInvers, orentations, orentationsInvert, rotations, rotationsInvert):
    sorce = pm.ls(sl = True)[0]
    
    if sorce is None:
        sys.stdout.write('Error: At least one joint must be selected.')
        return
    
    # Makes sure the joint selected is really the root joint:
    rootSorce = ReversedHierarchy(sorce)
    rootSorce = pm.ls(sl = True)[0]
    
    # Hierarchy Calculations:
    # Add root joint to the list first:
    hirarchy.append(rootSorce)
    # Add all roots children:
    Hirarchy(rootSorce, hirarchy)
    
    for s in hirarchy:
        tempParentMatrix = dt.Matrix()
        # For sorce:
        PerentRotAndOr(s, orient, jointsRoatations)
        tempParentMatrix = CalculateOriAndRot(orient, jointsRoatations)
        perentMatrixList.append(tempParentMatrix)
        perentMatrixListInvers.append(tempParentMatrix.inverse())
        
        orient[:] = []
        jointsRoatations[:] = []
    
    for h in hirarchy:
        pm.currentTime(0.0)
        rot = h.getRotation()
        rotation = dt.EulerRotation(rot).asMatrix()
        rotations.append(rotation)
        rotationsInvert.append(rotation.inverse())
    
    Orientations(hirarchy, orentations, orentationsInvert)
    
    sys.stdout.write('Info: Target skeleton hierarchy calculated.')

#================================================================================
#   TESTING 
#================================================================================
# Variables: 
"""hirarchy = []
orient = []
jointsRoatations = []

perentMatrixList = []
perentMatrixListInvers = []

orentations = []
orentationsInvert = []

rotations = []
rotationsInvert = []

jointNameList = []
jointMatrixesList = []

nrOFFramesAndJoints = []

HirarchyListCreator(hirarchy, orient, jointsRoatations, perentMatrixList, perentMatrixListInvers, orentations, orentationsInvert, rotations, rotationsInvert)
filePath = CreateFilePath()
WriteToFile(filePath, hirarchy, rotationsInvert, orentationsInvert, perentMatrixListInvers, perentMatrixList, orentations)"""