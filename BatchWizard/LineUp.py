import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)


print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)

scans = []
basemeshes = []
results = []
xdiff = 0

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):
    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan %s..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'])
    scans.append(scan)
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
    basemeshes.append(basemesh)
    print "OK"

    if 'basemeshTextureFileName' in task:
        print "Loading basemesh texture %s" % task['basemeshTextureFileName']
        basemesh.texture = wrap.Image(task['basemeshTextureFileName'])
        print "OK"
    else:
        print "No basemesh texture found"

    print "Rigid alignment basemesh to scan..."
    basemeshAlignPoints = wrap.loadPoints(task['basemeshAlignPointsFileName'])
    scanAlignPoints = wrap.loadPoints(task['scanAlignPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshAlignPoints, scan, scanAlignPoints, **task['methodsArgs']['rigidAlignment'])
    basemesh.transform(transformMatrix)

    scaleFactor = 10.0 / scan.boundingBoxSize[0]
    scan.scale(scaleFactor)
    basemesh.scale(scaleFactor)

    scan.translate(xdiff,0,0)
    basemesh.translate(xdiff,basemesh.boundingBoxSize[1],0)

    if os.path.exists(task['resultFileName']):
        print "Loading result %s..." % task['resultFileName']
        result = wrap.Geom(task['resultFileName'])
        results.append(result)
        print "OK"

        if 'resultTextureFileName' in task and os.path.exists(task['resultTextureFileName']):
            print "Loading texture %s" % task['resultTextureFileName']
            result.texture = wrap.Image(task['resultTextureFileName'])
            print "OK"
        else:
            print "No result texture found"

        result.scale(scaleFactor)
        result.translate(xdiff,basemesh.boundingBoxSize[1]*2,0)


    xdiff += scan.boundingBoxSize[0]

    wrap.fitToView()
    print

print "All objects here in the viewport are rigidly aligned and scaled to be the same width."
print "Lower row - scans, middle row - basemeshes, top row - wrapped results (if exist)."

