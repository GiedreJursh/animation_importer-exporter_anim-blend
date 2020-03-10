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

#==============================================================================

# Bake animations from layers to BaseAnimation
def BakeAnimations(hirarchy):
    for h in hirarchy:
        pm.select(h, replace=True)
        pm.bakeResults(t=(0,30))

# Finds Binary files
def OpenFiles():
    newerFile = pm.fileDialog2(ds = 2, ff = '*.sb', fm = 1)
    if(newerFile == None):
        sys.stdout.write('Warning: At lest one animation file must be selected.')
        return
    
    return newerFile

# Finds the actual name of animation on filie path
def FindAnimName(newerFile):
    nameString = str(newerFile)
    nameString = nameString.split("'")
    nameString = nameString[1]
    nameString = nameString.split("/")
    nameStringLenght =  len(nameString)
    nameString = nameString[nameStringLenght - 1]
    nameString = nameString.split(".")
    nameString = nameString[0]
    
    return nameString

# Loads binary files:
def ReadFromFiles(filePath, jointNameList, jointMatrixesList, nrOFFramesAndJoints):

    if(filePath[0] == None):
        sys.stdout.write('Error: File was never selected.')
        return
    
    importFile = open(filePath[0], 'rb')
    
    data = importFile.read()
    
    headerLen1 = 8 # 2 intiges at 4 bytes eatch
    
    res = struct.unpack('ii', data[0:headerLen1])
    
    nrOFFramesAndJoints.append(res[0])
    nrOFFramesAndJoints.append(res[1])
    
    newkPrimMatrixList =[]
    
    updatedLenght = headerLen1
    
    for w in range(0, nrOFFramesAndJoints[1]):
        
        newStart = updatedLenght
        
        jointTextLean = newStart + 4 # 1 intiger at 4 bytes eatch
        
        jointData = struct.unpack('i', data[newStart:jointTextLean])
        
        jointArrayLengd = jointData[0]
        
        jointName = jointTextLean + jointArrayLengd
        
        jointNameList.append(data[jointTextLean:jointName])
        
        del newkPrimMatrixList[:]
        
        updatedLenght = jointName
        
        for x in range(0, (nrOFFramesAndJoints[0] + 1)):
            
            matrixFloats = updatedLenght + (16 * 4) # 16 floats of size 4 eatch
            
            newkPrimList = struct.unpack('ffffffffffffffff', data[updatedLenght:matrixFloats])
            
            tempMatrix = dt.Matrix()
            
            updatedLenght = matrixFloats
    
            tempMatrix.a00 = newkPrimList[0]
            tempMatrix.a01 = newkPrimList[1]
            tempMatrix.a02 = newkPrimList[2]
            tempMatrix.a03 = newkPrimList[3]
            
            tempMatrix.a10 = newkPrimList[4]
            tempMatrix.a11 = newkPrimList[5]
            tempMatrix.a12 = newkPrimList[6]
            tempMatrix.a13 = newkPrimList[7]
            
            tempMatrix.a20 = newkPrimList[8]
            tempMatrix.a21 = newkPrimList[9]
            tempMatrix.a22 = newkPrimList[10]
            tempMatrix.a23 = newkPrimList[11]
            
            tempMatrix.a30 = newkPrimList[12]
            tempMatrix.a31 = newkPrimList[13]
            tempMatrix.a32 = newkPrimList[14]
            tempMatrix.a33 = newkPrimList[15]
    
            newkPrimMatrixList.append(tempMatrix)
    
        jointMatrixesList.append(newkPrimMatrixList[:])
        
    importFile.close()
    sys.stdout.write('Info: Animation successfully loaded.\n')

# Bakes animations in to layers
def CreateLayers(animLayerName, hirarchy, nrOfFrames, rotations, orent, orentInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesList, animLayerList):
    animLayer1 = pm.animLayer(animLayerName)
    animLayerList.append(animLayer1)
    
    for index, h in enumerate(hirarchy):
        
        pm.select(h, replace=True)
        
        pm.animLayer(animLayerName, edit=True, addSelectedObjects=True)
        
        # Loop through Keys: 
        for i in range(0, (nrOfFrames + 1)):
            
            # Get Final source rotation at this keyframe:
            pm.currentTime(i)
    
            kBiss = orent[index] * perentMatrixList[index] * jointMatrixesList[index][i] * perentMatrixListInvers[index] * orentInvert[index]
                    
            # Final rotation:
            finalRotation = rotations[index] * kBiss
            
            #=====================================================================
            # Get the right format for rotations:
            keyRotQ = dt.EulerRotation(finalRotation)
            keyRotDegree = dt.degrees(keyRotQ)
            
            #=====================================================================
            # Set rotations at current time:
            h.setRotation(keyRotDegree)
            
            # Save to keyframe:
            pm.setKeyframe(h, time = (i,i), edit = True, animLayer = animLayerName)
    
    #Set weights to 0.0 so they dont influence other layers when baked:        
    pm.animLayer(animLayerName, edit = True, w=0.0)
    sys.stdout.write('Info: Animation layers successfully created.\n')
        
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
    sys.stdout.write('Info: Target skeleton hierarchy calculated.\n')

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

nrOfFrames = 0
nrOfJoints = 0

# Functions: 
HirarchyListCreator(hirarchy, orient, jointsRoatations, perentMatrixList, perentMatrixListInvers, orentations, orentationsInvert, rotations, rotationsInvert)

filePath = OpenFiles()
animName = FindAnimName(filePath)

ReadFromFiles(filePath, jointNameList, jointMatrixesList, nrOFFramesAndJoints)

nrOfFrames = nrOFFramesAndJoints[0]
nrOfJoints = nrOFFramesAndJoints[1]

CreateLayers(animName, hirarchy, nrOfFrames, rotations, orentations, orentationsInvert, perentMatrixList, perentMatrixListInvers, jointMatrixesList)

BakeAnimations(hirarchy)"""