import wrap
import os

# This example is created as answer for question of owen at
# http://www.russian3dscanner.com/forum/index.php?topic=431.msg970#msg970
# 
# It shows usage of wrap.subset and wrap.applySubset commands while creating blendshapes
# When head scans are ideally aligned to each other by the skull, 
# there is no need to use subset since there will be no unintended global movement of the head.
# But in the cases when you need absolute no movement of some vertices you can use subsets.
#
# In this particular case we restrict movement of the back of the head.
#
# Subsets can be used not only in blendshapes but also for other cases
# like wrapping a full-body base mesh (with legs, arms, torso, head) to just the frontal part of a face mesh.
  

basemesh = wrap.Geom(wrap.demoModelsPath + "/AlexNeutral_3DHumanity_Wrapped.obj",scaleFactor = 1000)
basemesh.wireframe = False
basemesh.shaded = False
basemesh.texture = wrap.Image(wrap.demoModelsPath + "/AlexNeutral_3DHumanity_Wrapped.jpg")

basemeshPoints = wrap.loadPoints("BasemeshPoints.txt")
basemeshControlPoints = wrap.loadPoints("BasemeshControlPoints.txt")

scanFileName = wrap.demoModelsPath + "/AlexSmile_3DHumanity.obj"
textureFileName = wrap.demoModelsPath + "/AlexSmile_3DHumanity.jpg"
scanPoints = wrap.loadPoints("AlexSmilePoints.txt")
scanControlPoints = wrap.loadPoints("AlexSmileControlPoints.txt")

print "Processing: ", scanFileName
scan = wrap.Geom(scanFileName,scaleFactor = 1000)
scan.wireframe = False
scan.shaded = False
scan.texture = wrap.Image(textureFileName)

print "Rigid alignment..."
(scanPoints, basemeshPoints) = wrap.selectPoints(scan,basemesh,pointsLeft = scanPoints, pointsRight = basemeshPoints)
scan.transform(wrap.rigidAlignment(scan,scanPoints,basemesh,basemeshPoints,matchScale = False))
basemesh.fitToView()


print "Choose polygons of basemesh subset..."
subsetPolygons = wrap.loadPolygons("BasemeshSubsetPolygons.txt")
subsetPolygons = wrap.selectPolygons(basemesh, subsetPolygons)
(basemeshSubset,basemeshSubsetVertexMapping) = wrap.subset(basemesh, subsetPolygons)



# In the non-rigid registration we want to use control points previously generated for other examples.
# Subset creates new geom object which consists of some polygons of original, it's order of vertices is different.
# So we just retarget points to subset geometry 
basemeshSubsetControlPoints = []
for point in basemeshControlPoints:
    pointIn3D = basemesh.pointOnTriangleToPoint(point)
    subsetPoint = basemeshSubset.pointToPointOnTriangle(*pointIn3D)
    basemeshSubsetControlPoints.append(subsetPoint)


print "Non-rigid registration..."
(scanControlPoints,basemeshSubsetControlPoints) = wrap.selectPoints(scan,basemeshSubset,pointsLeft = scanControlPoints,pointsRight = basemeshSubsetControlPoints)
wrappedSubset = wrap.nonRigidRegistration(basemeshSubset,scan,basemeshSubsetControlPoints,scanControlPoints,minNodes = 20,initialRadiusMultiplier = 0.5,smoothnessFinal = 0.2)
wrapped = basemesh.copy()
wrap.applySubset(wrapped, wrappedSubset, basemeshSubsetVertexMapping)
wrapped.wireframe = True
basemesh.wireframe = True
basemeshSubset.hide()
wrappedSubset.hide()
scan.hide()

# These steps commented just for simplcity. You cans use them in real life as usual.
#print "Subdivision..."
#wrapped = wrap.subdivide(wrapped)
#print "Mesh projection..."
#wrapped = wrap.projectMesh(wrapped,scan,1,basemeshDisabledPolygons)

print "Texture transfer..."
wrapped.texture = wrap.transferTexture(scan,scan.texture,wrapped,(2048,2048),maxRelativeDist = 5)
wrapped.texture.extrapolate()

print "Saving results..."
wrapped.save("AlexSmile_Wrapped.obj",scaleFactor = 1 / 1000.0)
wrapped.texture.save("AlexSmile_Wrapped.jpg")

print "All done, presenting results..."
basemesh.wireframe = True
geoms = [wrapped, basemesh]
i = 0
while True:
    visibleIndex = i%2
    invisibleIndex = (visibleIndex + 1) % 2
    geoms[visibleIndex].show()
    geoms[invisibleIndex].hide()
    i += 1
    ans = wrap.customDialog("Loop results", ["Next","Stop"])
    if ans == "Stop":
        break

    
    
    
    
#basemesh.hide()
#basemesh.show()
