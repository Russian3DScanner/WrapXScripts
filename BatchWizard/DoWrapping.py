import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):

    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'])
    scan.wireframe = False
    print "OK"

    if 'textureFileName' in task:
        print "Loading texture '%s'" % task['textureFileName']
        scan.texture = wrap.Image(task['textureFileName'])
        print "OK"
    else:
        print "No texture found"

    print "Loading basemesh '%s'..." % task['basemeshFileName']
    basemesh = wrap.Geom(task['basemeshFileName'])
    print "OK"

    #if 'basemeshTextureFileName' in task:
    #    print "Loading basemesh texture %s" % task['basemeshTextureFileName']
    #    basemesh.texture = wrap.Image(task['basemeshTextureFileName'])
    #    print "OK"
    #else:
    #    print "No basemesh texture found"    

    print "Rigid alignment..."
    basemeshPoints = wrap.loadPoints(task['basemeshPointsFileName'])
    scanPoints = wrap.loadPoints(task['scanPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshPoints, scan, scanPoints, **task['methodsArgs']['rigidAlignment'])
    basemesh.transform(transformMatrix)
    wrap.fitToView()
    print "OK"

    print "Non-rigid registration..."
    minScanSize = min(scan.boundingBoxSize)
    minBaseSize = min(basemesh.boundingBoxSize)

    if minBaseSize < 1.0 and minBaseSize < minScanSize:
        scaleDegree = 10.0/minBaseSize
    elif minScanSize < 1.0:
        scaleDegree = 10.0/minScanSize
    else:
        scaleDegree = 1.0

    if scaleDegree > 1.0:
        print "Scan is too small, temporarily increase scale to avoid rounding errors. Scale: %f" % scaleDegree
        scan.scale(scaleDegree)
        basemesh.scale(scaleDegree)
    scan.fitToView()

    wrapped = wrap.nonRigidRegistration(basemesh,scan,basemeshPoints,scanPoints, **task['methodsArgs']['nonRigidRegistration'])
    basemesh.hide()
    print "OK"

    if scaleDegree > 1.0:
        print "Restoring original scan scale"
        wrapped.scale(1.0/scaleDegree)
        scan.scale(1.0/scaleDegree)

    wrapped.fitToView()

    print "Saving results..."
    if not os.path.exists(os.path.dirname(task['wrappedResultFileName'])):
        try: os.mkdir(os.path.dirname(task['wrappedResultFileName']))
        except: pass

    wrapped.save(task['wrappedResultFileName'])
    print "Wrapped result saved to '%s'" % task['wrappedResultFileName']

print
print "Wrapping done, please use 'doPostProcessing.py' to make post processing"
print "or 'ShowResults.py' to see all results"
print

