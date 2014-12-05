import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is %s" %  configFile

tasks = ParseConfig.parseConfig(configFile)

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):
    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan %s..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'])
    scan.wireframe = False
    print "OK"

    if 'textureFileName' in task:
        print "Loading texture %s" % task['textureFileName']
        scan.texture = wrap.Image(task['textureFileName'])
        print "OK"
    else:
        print "No texture found"

    print "Loading basemesh %s..." % task['basemeshFileName']
    basemesh = wrap.Geom(task['basemeshFileName'])
    print "OK"

    print "Rigid alignment..."
    basemeshAlignPoints = wrap.loadPoints(task['basemeshAlignPointsFileName'])
    scanAlignPoints = wrap.loadPoints(task['scanAlignPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshAlignPoints, scan, scanAlignPoints, **task['methodsArgs']['rigidAlignment'])
    basemesh.transform(transformMatrix)
    wrap.fitToView()
    print "OK"    

    print "Non-rigid registration..."
    basemeshWrapPoints = wrap.loadPoints(task['basemeshWrapPointsFileName'])
    scanWrapPoints = wrap.loadPoints(task['scanWrapPointsFileName'])
    
    minScanSize = min(scan.boundingBoxSize)    
    minBaseSize = min(basemesh.boundingBoxSize)    
        
    if minBaseSize < 1.0 and minBaseSize < minScanSize:
        scaleDegree = 10.0/minBaseSize
    elif minScanSize < 1.0:
        scaleDegree = 10.0/minScanSize
    else:
        scaleDegree = 1.0    

    if scaleDegree > 1.0:
        print "Scan or base mesh are too small, temporary increase scale to avoid round errors. Scale: %f" % scaleDegree
        scan.scale(scaleDegree)
        basemesh.scale(scaleDegree)
    scan.fitToView()
    
    wrapped = wrap.nonRigidRegistration(basemesh,scan,basemeshWrapPoints,scanWrapPoints, **task['methodsArgs']['nonRigidRegistration'])
    basemesh.hide()
    print "OK"
    
    # Comment next three lines if you want to save basemesh topology unchanged
    if 'subdivide' not in task['useMethods'] or task['useMethods']['subdivide']:
        print "Subdivision..."
        wrapped = wrap.subdivide(wrapped, **task['methodsArgs']['subdivide'])
        print "OK"
    else:
        print 'Skip subdivide'
    
    if 'projectMesh' not in task['useMethods'] or task['useMethods']['projectMesh']:
        print "Extracting details..."
        wrapped = wrap.projectMesh(wrapped, scan, **task['methodsArgs']['projectMesh'])
        print "OK"
    else:
        print 'Skip projectMesh'

    print "Saving results..."
    if not os.path.exists(os.path.dirname(task['resultFileName'])):
        try: os.mkdir(os.path.dirname(task['resultFileName'])) 
        except: pass
        
    if scaleDegree > 1.0:
        wrapped.scale(1.0/scaleDegree)
        scan.scale(1.0/scaleDegree)
    
    wrapped.fitToView()
    
    wrapped.save(task['resultFileName'])
    print "Wrapped result saved to %s" % task['resultFileName']
    
    if scan.texture:
        wrapped.texture = wrap.transferTexture(scan, scan.texture, wrapped)        
        wrapped.texture.extrapolate()        
        wrapped.texture.save(task['resultTextureFileName'])
        print "Wrapped result texture saved to %s" % task['resultTextureFileName']

    print
    
print "Wrapping done, please use LineUp.py to see all results"