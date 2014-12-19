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
wrappedResults = []
postprocResults = []
xdiff = 0

tasksCount = len(tasks)
taskNum = 0
#for taskNum, task in enumerate(tasks):

print "All objects here in the viewport are rigidly aligned and scaled to be the same width."
print "From bottom:"
print "1st row (lower) - scans"
print "2nd row - basemeshes"
print "3rd row - wrapped basemeshes (if exist)"
print "4th row (top) - postprocessed wrapped basemeshes (if exist)"

while True:

    task = tasks[taskNum]

    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'])
    wrap.fitToView()
    #scans.append(scan)
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
    wrap.fitToView()
    #basemeshes.append(basemesh)
    print "OK"

    if 'basemeshTextureFileName' in task:
        print "Loading basemesh texture '%s'" % task['basemeshTextureFileName']
        basemesh.texture = wrap.Image(task['basemeshTextureFileName'])
        print "OK"
    else:
        print "No basemesh texture found"

    print "Rigid alignment basemesh to scan..."
    basemeshPoints = wrap.loadPoints(task['basemeshPointsFileName'])
    scanPoints = wrap.loadPoints(task['scanPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshPoints, scan, scanPoints, **task['methodsArgs']['rigidAlignment'])
    basemesh.transform(transformMatrix)
    wrap.fitToView()

    scaleFactor = 10.0 / scan.boundingBoxSize[0]
    scan.scale(scaleFactor)
    basemesh.scale(scaleFactor)

    scan.translate(xdiff,0,0)
    basemesh.translate(xdiff,basemesh.boundingBoxSize[1],0)

    if os.path.exists(task['wrappedResultFileName']):
        print "Loading wrapped basemesh '%s'..." % task['wrappedResultFileName']
        wrappedResult = wrap.Geom(task['wrappedResultFileName'])
        wrap.fitToView()
        #wrappedResults.append(result)
        print "OK"

        wrappedResult.scale(scaleFactor)
        wrappedResult.translate(xdiff,basemesh.boundingBoxSize[1]*2,0)


    if os.path.exists(task['postprocResultFileName']):
        print "Loading wrapped basemesh '%s'..." % task['postprocResultFileName']
        postprocResult = wrap.Geom(task['postprocResultFileName'])
        wrap.fitToView()
        #postprocResults.append(result)
        print "OK"

        if 'postprocResultTextureFileName' in task and os.path.exists(task['postprocResultTextureFileName']):
            print "Loading texture '%s'" % task['postprocResultTextureFileName']
            postprocResult.texture = wrap.Image(task['postprocResultTextureFileName'])
            print "OK"
        else:
            print "No result texture found"

        postprocResult.scale(scaleFactor)
        postprocResult.translate(xdiff,basemesh.boundingBoxSize[1]*3,0)


    xdiff += scan.boundingBoxSize[0]

    wrap.fitToView()

    title = "scan %d/%d    %s" % (taskNum+1, len(tasks), os.path.basename(task['scanFileName']))
    buttons = ["Stop"]
    if taskNum != (len(tasks)-1):
        buttons.insert(0,"Next ->")
    if taskNum > 0:
        buttons.insert(0,"<- Prev")
    ans = wrap.customDialog(title, buttons)

    if ans == "Stop":
        print "Stopped"
        break
    elif ans == "<- Prev":
        taskNum -= 1
    elif ans == "Next ->":
        taskNum += 1

    del scan
    del basemesh
    if 'wrappedResult' in locals(): del wrappedResult
    if 'postprocResult' in locals(): del postprocResult



