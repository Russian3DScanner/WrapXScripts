import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)
basemesh = None
scan = None

for taskNum, task in enumerate(tasks):

    if basemesh: del basemesh
    if scan: del scan
    wrap.fitToView()

    print "Task %d of %d" % (taskNum + 1, len(tasks))
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'], scaleFactor = 1000)
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

    if 'basemeshTextureFileName' in task:
        print "Loading basemesh texture '%s'" % task['basemeshTextureFileName']
        basemesh.texture = wrap.Image(task['basemeshTextureFileName'])
        print "OK"
    else:
        print "No basemesh texture found"

    # Rigid alignment
    basemeshPoints = []
    if os.path.exists(task['basemeshPointsFileName']):
        basemeshPoints = wrap.loadPoints(task['basemeshPointsFileName'])

    scanPoints = []
    if os.path.exists(task['scanPointsFileName']):
        scanPoints = wrap.loadPoints(task['scanPointsFileName'])


    accepted = False
    basemesh.hide()

    while not accepted:
        print
        print "Select THREE AT LEAST point correspondences between basemesh and scan..."
        (basemeshPoints, scanPoints) = wrap.selectPoints(basemesh, scan, basemeshPoints, scanPoints)
        print "OK"

        transformMatrix = wrap.rigidAlignment(basemesh, basemeshPoints, scan, scanPoints, **task['methodsArgs']['rigidAlignment'])
        transformedBasemesh = basemesh.copy()
        transformedBasemesh.transform(transformMatrix)
        wrap.fitToView()
        print "Is rigid alignment OK?"
        ans = wrap.customDialog("Is rigid alignment OK?", ("No","Yes"))
        accepted = (ans == "Yes")
        if accepted:
            print "Yes"
        else:
            print "Rigid alignment not accepted, let's repeat point selection."


    basemesh = transformedBasemesh
    del transformedBasemesh

    # save
    basemeshPointsDir = os.path.dirname(task['basemeshPointsFileName'])
    if not os.path.exists(basemeshPointsDir):
        print "Creating directory '%s'" % basemeshPointsDir
        os.makedirs(basemeshPointsDir)
    wrap.savePoints(basemeshPoints,task['basemeshPointsFileName'])

    scanPointsDir = os.path.dirname(task['scanPointsFileName'])
    if not os.path.exists(scanPointsDir):
        print "Creating directory '%s'" % scanPointsDir
        os.makedirs(scanPointsDir)
    wrap.savePoints(scanPoints,task['scanPointsFileName'])
    print "Point correspondences saved"



print
print "Point correspondences saved, please run 'DoWrapping.py'."
print "For showing aligned scans and basemeshes run 'ShowResults.py'."
print

