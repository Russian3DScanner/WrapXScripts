import wrap
import sys,os
import datetime

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile, 'DefaultSettings_2_Wrapping.txt')

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):

    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'], fitToView = False)
    scan.wireframe = False
    scaleFactor = 100.0 / scan.boundingBoxSize[0]
    scan.scale(scaleFactor)
    wrap.fitToView()
    print "OK"

    if 'textureFileName' in task:
        print "Loading texture '%s'" % task['textureFileName']
        scan.texture = wrap.Image(task['textureFileName'])
        print "OK"
    else:
        print "No texture found"

    print "Loading basemesh '%s'..." % task['basemeshFileName']
    basemesh = wrap.Geom(task['basemeshFileName'], fitToView = False)
    print "OK"

    print "Rigid alignment..."
    basemeshPoints = wrap.loadPoints(task['basemeshPointsFileName'])
    scanPoints = wrap.loadPoints(task['scanPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshPoints, scan, scanPoints, matchScale = True)
    basemesh.transform(transformMatrix)
    print "OK"

    print "Non-rigid registration..."
    freePolygons = []
    if os.path.exists(task['freePolygonsFileName']):
        print "Using free polygons from %s", task['freePolygonsFileName']
        freePolygons = wrap.loadPolygons(task['freePolygonsFileName'])
    else:
        print "No free polygons"
    
    
    start = datetime.datetime.now()
    wrapped = wrap.nonRigidRegistration(basemesh,scan,basemeshPoints,scanPoints,freePolygons, **task['methodsSettings']['nonRigidRegistration'])
    end = datetime.datetime.now()
    print "OK, took ", (end-start).total_seconds(), " seconds"
    del basemesh
    
    print "Saving results..."
    if not os.path.exists(os.path.dirname(task['wrappedResultFileName'])):
        try: os.mkdir(os.path.dirname(task['wrappedResultFileName']))
        except: pass

    wrapped.save(task['wrappedResultFileName'], scaleFactor = 1.0/scaleFactor)
    print "Wrapped result saved to '%s'" % task['wrappedResultFileName']
    print

print
print "Wrapping done, please use '3_PostProcessing.py' to make post processing"
print "or 'ShowResults_2_Wrapping.py' to see all results"
print

