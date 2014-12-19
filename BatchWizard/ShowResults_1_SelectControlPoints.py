import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)


print "Select config file"
#configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
configFile = '/home/ivan/WrapXScripts/BatchWizard/00_output/Config_Scans_Basemeshes.txt'
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)

scans = []
basemeshes = []
wrappedResults = []
postprocResults = []

taskNum = 0

while True:

    task = tasks[taskNum]

    print "Task %d of %d" % (taskNum + 1, len(tasks))
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

    if 'basemeshTextureFileName' in task:
        print "Loading basemesh texture '%s'" % task['basemeshTextureFileName']
        basemesh.texture = wrap.Image(task['basemeshTextureFileName'])
        print "OK"
    else:
        print "No basemesh texture found"

    print "Rigid alignment basemesh to scan..."
    basemeshPoints = wrap.loadPoints(task['basemeshPointsFileName'])
    scanPoints = wrap.loadPoints(task['scanPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshPoints, scan, scanPoints, matchScale = True)
    basemesh.transform(transformMatrix)
    print "OK"
    print

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



